import argparse
import os.path
from datetime import timedelta, date

import git
import xlsxwriter

basedir = os.path.dirname(__file__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--projects", "-p", nargs="+", help="project dir can be list", required=True)
    parser.add_argument("--author", "-a", help="author pattern name use for filter", required=True)
    parser.add_argument("--month", "-m", type=int, help="number month of year", required=True)
    parser.add_argument("--output-file", "-o", help="export file name", required=True)
    args = parser.parse_args()

    # f = open(os.path.join(basedir, "test.txt"), 'w')
    records = {}
    since = date(2021, args.month, 1)
    until = date(since.year + since.month // 12, since.month % 12 + 1, 1) - timedelta(days=1)
    limit = (f"--since={since}", f"--until={until}")

    for i in range(until.day):
        dt = date(2021, args.month, 1).replace(day=i + 1)
        records[dt.strftime("%Y-%m-%d")] = ""
    # prepare data
    for project in args.projects:
        repo = git.Git(project)
        result = repo.log(f"--author={args.author}", "--format=%ai|%an|%s", "--all", *limit)
        lines = result.split("\n")
        for line in lines:
            try:
                _date, name, activity = line.split("|")
                _date = _date.split(" ")[0]
                if records.get(_date):
                    records[_date] = records.get(_date) + "\n" + activity
                else:
                    records[_date] = activity
            except:
                pass

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(args.output_file)
    worksheet = workbook.add_worksheet()

    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 50)
    # Add a bold format to use to highlight cells.
    worksheet.write(0, 0, "Date")
    worksheet.write(0, 1, "Activity")
    for i, (k, v) in enumerate(records.items()):
        worksheet.write(i + 1, 0, k)
        worksheet.write(i + 1, 1, v)
    workbook.close()

    print("Export success to", args.output_file)


if __name__ == '__main__':
    main()
