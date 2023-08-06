import json

import click


class TSV(object):
    def __init__(self, filename, sep='\t', comment=None, limit=None, header=True, **kwargs):
        self.filename = filename
        self.sep = sep
        self.limit = limit
        self.header = header
        self.comment = comment

    def read(self, filename, sep='\t', comment=None, limit=None, header=True):

        with open(filename) as f:
            num = 0
            for line in f:
                if comment and line.startswith(comment):
                    continue
                linelist = line.strip().split(sep)

                num += 1
                
                if header and num == 1:
                    title = linelist
                    continue

                if header:
                    if len(title) != len(linelist):
                        msg = click.style('column number of row {} not match with title'.format(num), fg='red')
                        raise Exception(msg)
                    yield dict(zip(title, linelist))
                else:
                    yield linelist
    
                if limit and num >= limit:
                    break

    @property
    def data(self):
        res = self.read(self.filename,
                      sep=self.sep,
                      comment=self.comment,
                      limit=self.limit,
                      header=self.header)

        return list(res)

    def to_json(self, outfile=None, indent=2):
        if outfile:
            with open(outfile, 'w') as out:
                json.dump(self.data, out, ensure_ascii=False, indent=indent)
        else:
            return json.dumps(self.data, ensure_ascii=False, indent=indent)


if __name__ == "__main__":
    # tsv = TSV('examples/demo.tsv', limit=3, header=False)
    # tsv = TSV('examples/demo.tsv', header=False)
    # tsv = TSV('examples/demo.tsv')

    tsv = TSV('examples/demo.csv', sep=',')

    print(tsv.data)

    # print(tsv.to_json(indent=4))
    # print(tsv.to_json(indent=None))
    print(tsv.to_json())

    # tsv.to_json(outfile='out.json')
