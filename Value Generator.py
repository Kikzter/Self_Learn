import os
import re
import pandas
import time

valid_literals = [
    'g', 'gram',
    'gr', 'gm',
    'grams', 'gms',
    'kg', 'kilogram',
    'kgs', 'kilograms',
    'ml', 'milliliter', 'milliliters',
    'l', 'ltr', 'liter', 'liters',
    'oz', 'ounce', 'ounces', '-oz', '-ounce', '-ounces', 'pound'

]

gram_related = {"g": "kg", "gm": "kg", "gram": "kg", "grams": "kg", "gr": "kg", "ml": "l", "milliliter": "l",
                "milliliters": "l"}


class ScrapData:

    def __init__(self):
        self.i = 0

    def check_next_occurence_as_protien(self, index, ls):

        if index + 1 < len(ls):
            print("######" , ls[index+1])
            if ls[index + 1] == "protein":
                return False
            if ls[index+1] == "of":
                return  self.check_next_occurence_as_protien(index+1,ls)
        return True

    def loop_through(self, text):
        text = text.replace("(", " ").replace(")", " ").replace(",", "").replace("x" ," ")
        text = text.split(" ")
        possible_units = []
        i = 0
        # print("splitted", text)
        while i < len(text):
            txt = text[i]
            pattern_for_number = re.compile("[0-9.]+")
            pattern_for_text = re.compile("[a-z]+")
            matched_text_for_number = re.findall(pattern_for_number, txt)
            matched_text_for_text = re.findall(pattern_for_text, txt)
            # print(matched_text_for_text, matched_text_for_number, "%%%%%%")
            if len(matched_text_for_number) > 0:
                # print(matched_text_for_text, matched_text_for_number, "%%%%%%")

                if len(matched_text_for_text) > 0:
                    if matched_text_for_text[0].strip() in valid_literals:
                        op = self.check_next_occurence_as_protien(ls=text, index=i)
                        print(op , txt)
                        if op:
                            possible_units.append(txt)

                else:
                    if i + 1 < len(text) and text[i + 1].strip() in valid_literals:
                        if self.check_next_occurence_as_protien(ls=text, index=i):
                            possible_units.append(txt + text[i + 1])

            i += 1
        print(possible_units,"-------------")
        return possible_units

    def call_to_units(self, text):
        text = text.lower().replace("/" , " ").replace("|" ," ")
        return self.loop_through(text)

    

    def call_to_pack(self, text):
        x_text = text
        text = text.lower().replace("(", "").replace(")" ,"")
        if ("pack of" in text):
            # split the data using pack of
            text = text.replace(" ", "")
            # print(text,"pack")
            reg_ex_pattern = re.compile("packof[0-9]+")
            matched_data = re.findall(reg_ex_pattern, text)
            return re.findall(r"[0-9]+", matched_data[0])[0]
        else:
            text = x_text.replace(" ","")
            # print(text,"pack")
            reg_ex_pattern = re.compile("[0-9]+X")
            reg_ex_pattern2 = re.compile("X[0-9]+")

            matched_data = re.findall(reg_ex_pattern, text)
            matched_data2 = re.findall(reg_ex_pattern2, text)
            if len(matched_data) > 0:
                return re.findall(r"[0-9]+", matched_data[0])[0]
            if len(matched_data2) > 0 :
                return re.findall(r"[0-9]+", matched_data2[0])[0]
        return False

    def format_unit_pack(self, unit, pack):
        # unit_list =
        unit_list = []
        pattern_for_number = re.compile("[0-9.]+")
        pattern_for_text = re.compile("[a-z]+")
        matched_text_for_number = re.findall(pattern_for_number, unit)
        matched_text_for_text = re.findall(pattern_for_text, unit)
        print("^^^^" , matched_text_for_number ,matched_text_for_text)
        for i in range(0, len(matched_text_for_text)):
            unit_text = matched_text_for_text[i].strip()
            # print(gram_related.get(unit_text))
            ''' determine if they are in grams
            '''
            global unit_number
            unit_number = 0
            print(matched_text_for_number[i])
            if "." in matched_text_for_number[i].strip():

                unit_number = float(matched_text_for_number[i].strip())
            else:
                unit_number = int(matched_text_for_number[i].strip())

            if gram_related.get(unit_text) != None:
                if unit_number >= 1000:
                    convert_to_kg = unit_number / 1000
                    if unit_number % 1000 == 0:
                        convert_to_kg = int(unit_number / 1000)
                    # print("convert tonkg" , convert_to_kg,unit_number)
                    unit_list.append(str(convert_to_kg) + " " + gram_related.get(unit_text))
                else:
                    unit_list.append(matched_text_for_number[i].strip() + " " + matched_text_for_text[i].strip())
            else:
                unit_list.append(matched_text_for_number[i].strip() + " " + matched_text_for_text[i].strip())

        # print("## matched_text_for_number" , matched_text_for_number)
        # print("## matched_text_for_text", matched_text_for_text)
        formated_string = " "
        for ls in unit_list:
            formated_string = formated_string + ls + " (Pack of " + pack + ")"
        return formated_string.strip()

    #   for string in matched_str:

    def read_parse_write_csv_data(self):
        csv_file_desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'), 'sample.csv')

        data_file = {}
        df = pandas.read_csv(csv_file_desktop_path, index_col="ASIN").to_dict()["items"]
        i = 1
        for ls in df:
            # if i <= 1:
                data_file[ls] = [" "] * 5
                data_file[ls][0] = ls
                data_file[ls][1] = df[ls]
            # i+=1

        for data in data_file:

                print("-------------------")
                op = self.call_to_units(data_file[data][1])
                pack = self.call_to_pack(data_file[data][1])
                global  UOM
                global Pack
                UOM = ""
                Pack = ""
                print("*************")
                if len(op) > 0:
                    data_file[data][2] = " ".join(op)
                    UOM = " ".join(op)
                    if pack == False:
                        data_file[data][3] = "1"
                        Pack = "1"
                    else:
                        data_file[data][3] = pack
                        Pack = pack
                else:
                    if pack != False:
                        data_file[data][3]  = pack
                if len(op) > 0:
                    data_file[data][4] = self.format_unit_pack(UOM, Pack)

                

        # columns = ('items', 'UOM', 'pack', 'size_name')
        col_data = []
        for datas in data_file:
            col_data.append(data_file[datas])
        print(col_data)
        df = pandas.DataFrame(col_data , columns=['ASIN','Items', 'UOM' , "Pack" , "Size_name"])
        print(df)

        milliseconds = str(int(round(time.time() * 1000)))
        df.to_csv(os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'), "data" + milliseconds + ".csv") , index=False)


ScrapData().read_parse_write_csv_data()



