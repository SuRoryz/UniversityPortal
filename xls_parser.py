import xlrd

WORKING_DAYS = ["Понедельник", "Вторник", "Среда", "Четверг" ,"Пятница" ,"Суббота"]

class Parser:
    @staticmethod
    def parse_xls(filepath):
        book = xlrd.open_workbook(filepath)
        groups = book.sheet_names()

        result = {}
        for group in groups:
            shleude = book.sheet_by_name(group)
            result[group] = {}

            for day in WORKING_DAYS:

                sh_day = []

                for i in range(5):
                    try:
                        subj = shleude.cell_value(colx=WORKING_DAYS.index(day) + 2, rowx=(1+i*3)+0)
                        aud = shleude.cell_value(colx=WORKING_DAYS.index(day) + 2, rowx=(1+i*3)+1)
                        teach = shleude.cell_value(colx=WORKING_DAYS.index(day) + 2, rowx=(1+i*3)+2)
                    except:
                        break;
                    

                    sh_day.append({"subject": subj, "aud": aud, "teacher": teach})
                
                if not(sh_day):
                    break;

                result[group][day] = sh_day
    
        return result
        
#print(Parser.parse_xls("rasp.xls"))