import csv 
import json 

class EmailValidator(): 

    def __init__(self, email):
        self.email = email 

    def check_first_condition(self): 

        if '@' in self.email: 
            return True 
        else: 
            return False 
        
    def second_condition(self): 

        if '.' in self.email: 
            return True 
        else: 
            return False
        
    def vaildate(self): 

        if self.check_first_condition() and self.second_condition(): 
            return "given email is valid" 
        else: 
            return "given email is invalid" 
        
    def get_domain(self): 

        domain = ''

        flag = False 

        for char in self.email: 
            
            if flag: 
                domain+=char

            if char == '@': 
                flag = True 

        return domain 
    
    def get_domain_2(self): 

        domain = self.email.split('@')[1]

        return domain 
    
    def get_domain_3(self): 

        domain = self.email.rstrip("@")

        return domain

def read_csv_convert_json(filename): 

    

    with open(filename, 'r') as f: 

        reader = csv.DictReader(f)

        rows = list(reader)

    with open('student_data.json', 'w') as output_file: 

        json.dump(rows, output_file, indent=2)



        
def main(): 

    e=EmailValidator('Meghana@gmail.com')
    print(e.vaildate())
    print(e.get_domain())
    print(e.get_domain_2())
    print(e.get_domain_3())

    read_csv_convert_json('data.csv')

if __name__ == '__main__': 

    main()