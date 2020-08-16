from utilities.SqlParser import *
from utilities.main.entities.PojoAndDtoGenerator import *
from utilities.test.entities.PojoAndDtoTestGenerator import *
from configuration.Configuration import *
class SqlParserTester:

    def __init__(self):
        self.pojo_maker = PojoAndDtoGenerator()
        self.pojo_tester = PojoAndDtoTestGenerator()
        self.tablenames = []
        self.tabledata = {}

    def run(self):
        outputfile = open(Configuration.destinationtestfile, "w")
        parser = SqlParser(self.tablenames,self.tabledata)
        self.tablenames, self.tabledata = parser.processSQL(Configuration.sourcesqlfile)
        for table in self.tablenames:
            currenttable = self.tabledata[table]
            print("TABLE NAME = " + table)
            outputfile.write("TABLE NAME = " + table + ":\n")
            print("number of primary keys = " + str(len(currenttable.primarykeys)))
            outputfile.write("number of primary keys = " + str(len(currenttable.primarykeys)) + "\n")
            print("number of foreign keys = " + str(len(currenttable.fksymbolnames)))
            outputfile.write("number of foreign keys = " + str(len(currenttable.fksymbolnames)) + "\n")
            for pkfield in currenttable.primarykeys:
                print("primary key : " + pkfield)
                outputfile.write("primary key : " + pkfield + "\n")
                if len(currenttable.primarykeys) > 1:
                    print(pkfield + " is part of acompund primary key")
                    outputfile.write(pkfield + " is part of a compund primary key\n")
            for symbol in currenttable.fksymbolnames:
                print("symbol = " + symbol)
                outputfile.write("symbol = " + symbol + "\n")
                data = currenttable.fksymboldata[symbol]
                for datapoint in data:
                    print("symbol " + symbol + " specifications : field = " + datapoint[0] + " , parent table = " +
                          datapoint[1] + " , parent field = " + datapoint[2])
                    outputfile.write(
                        "symbol " + symbol + " specifications : field = " + datapoint[0] + " , parent table = " +
                        datapoint[1] + " , parent field = " + datapoint[2] + "\n")
            for symbol in currenttable.parentkeysymbolnames:
                print("PARENT for symbol = " + symbol)
                outputfile.write("symbol = " + symbol + "\n")
                data = currenttable.parentkeysymboldata[symbol]
                for datapoint in data:
                    print("PARENT symbol " + symbol + " specifications : field = " + datapoint[2] + " , child table = " +
                          datapoint[1] + " , child field = " + datapoint[0])
                    outputfile.write(
                        "PARENT symbol " + symbol + " specifications : field = " + datapoint[2] + " , child table = " +
                        datapoint[1] + " , child field = " + datapoint[0] + "\n")
            count = 1
            for list in currenttable.uniquekeys:
                print("unique keys count = " + str(count))
                outputfile.write("unique keys count = " + str(count) + "\n")
                for data in list:
                    print("unique key field = " + data)
                    outputfile.write(
                        "unique key field = " + data + "\n")
                count += 1
        print("TRIPLE CHECK")
        outputfile.write("\n\n*** TRIPLE CHECK ***\n\n")
        for table in self.tablenames:
            print("TABLE NAME = " + table)
            outputfile.write("TABLE NAME = " + table + "\n")
            currenttable = self.tabledata[table]
            for fieldname in currenttable.fieldnames:
                fielddata = currenttable.fielddata[fieldname]
                print("field name = " + fieldname + " , PK = " + str(fielddata.isprimary) + " , FK = " + str(
                    fielddata.isforeignkey) + " , parent key = " + str(fielddata.isparentkey) + " , UK = " + str(fielddata.unique))
                outputfile.write("field name = " + fieldname + " , PK = " + str(fielddata.isprimary) + " , FK = " + str(
                    fielddata.isforeignkey) + " , parent key = " + str(fielddata.isparentkey)+ " , UK = " + str(fielddata.unique) + "\n")
        print("DONE")
        outputfile.close()

        """
            testing the Entity Pojos
        """
        src = "pojo"
        for table in self.tablenames:
            currenttable = self.tabledata[table]
            currenttable.topmainpackage = "/temp"
            currenttable.toptestpackage = "/temp"
            self.pojo_maker.create_pojo_and_dto_classes(currenttable, src, self.tabledata)
            self.pojo_maker.create_pojo_and_dto_classes(currenttable, "dto", self.tabledata)
            self.pojo_tester.create_pojo_test_class(currenttable,"pojo",self.tabledata)

if __name__ == '__main__':
    tester = SqlParserTester()
    tester.run()
