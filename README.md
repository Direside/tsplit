# tsplit

Split up tests into even buckets based on a junit xml file.

## Usage

`./tsplit/tsplit.py -g 10 -o tests/test_data/GROUP tests/test_data/report.xml`

### Options

    -g --groups NUMBER  Number of groups to split the tests into. Defaults to 4.
    -o --output PREFIX  Output to file with the given prefix followed by the number. E.g. GROUP would output [ GROUP1, GROUP2, GROUP3, GROUP4 ]
    -e --env    PREFIX  Output to an enviroment variable with the given prefix followed by the number. See above.
