from ..table_utils import Table, Grouping

class PeopleFixture(object):
    """This fixture represents data imported using import_people()"""
    def __init__(self, l, categories):
        self.people = l
        self.categories = categories
        

big_people_fixture = PeopleFixture([{'Category': 'Health Administration',
                                     'Wed': '', 'Last Name': 'Arrington',
                                     'Fri': '', 'Tue': '', 'Thu': '',
                                     'First Name': 'Barbara', 'Mon': ''},
                                    {'Category': 'Health Administration',
                                     'Wed': '', 'Last Name': 'Brannon',
                                     'Fri': '1', 'Tue': '', 'Thu': '',
                                     'First Name': 'Diane', 'Mon': ''},
                                    {'Category': 'Health Administration',
                                     'Wed': '', 'Last Name': 'Caron',
                                     'Fri': '', 'Tue': '', 'Thu': '',
                                     'First Name': 'Rosemary', 'Mon': ''},
                                    {'Category': 'Health Administration',
                                     'Wed': '', 'Last Name': 'Clement',
                                     'Fri': '', 'Tue': '', 'Thu': '',
                                     'First Name': 'Dolores', 'Mon': ''},
                                    {'Category': 'Health Administration',
                                     'Wed': '', 'Last Name': 'Diana',
                                     'Fri': '', 'Tue': '', 'Thu': '',
                                     'First Name': 'Mark', 'Mon': ''},
                                    {'Category': 'Health Administration',
                                     'Wed': '', 'Last Name': 'Gelmon',
                                     'Fri': '', 'Tue': '', 'Thu': '',
                                     'First Name': 'Sherril', 'Mon': ''},
                                    {'Category': 'Health Administration',
                                     'Wed': '', 'Last Name': 'Gentry', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Daniel', 'Mon': '1'}, {'Category': 'Health Administration', 'Wed': '', 'Last Name': 'Grazier', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Kyle', 'Mon': ''}, {'Category': 'Health Administration', 'Wed': '', 'Last Name': 'Hatcher', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Paige', 'Mon': ''}, {'Category': 'Health Administration', 'Wed': '', 'Last Name': 'Johnson', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Christopher', 'Mon': ''}, {'Category': 'Health Administration', 'Wed': '1', 'Last Name': 'Lee', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Bob', 'Mon': ''}, {'Category': 'Health Administration', 'Wed': '', 'Last Name': 'Mittler', 'Fri': '', 'Tue': '1', 'Thu': '', 'First Name': 'Jessica', 'Mon': ''}, {'Category': 'Health Administration', 'Wed': '', 'Last Name': "O'Connor", 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Stephen', 'Mon': ''}, {'Category': 'Health Administration', 'Wed': '', 'Last Name': 'Restuccia', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Joseph', 'Mon': ''}, {'Category': 'Health Administration', 'Wed': '', 'Last Name': 'Robbins', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Cathy', 'Mon': ''}, {'Category': 'Health Administration', 'Wed': '', 'Last Name': 'Stefl', 'Fri': '', 'Tue': '', 'Thu': '1', 'First Name': 'Mary', 'Mon': ''}, {'Category': 'Health Administration', 'Wed': '', 'Last Name': 'Wakefield', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Douglas', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Alessandrini', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Evie', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Andersson-G_re', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Boel', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Barach', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Paul', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Batalden', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Maren', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Batalden', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Paul', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Baum', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Karyn', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Bowen', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Judith', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Coleman', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Mary', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Englander', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Bob', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Fish', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Jason', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Foster', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Tina', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Frankel', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Richard', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Galbraith', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Robert', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Geltman', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Joshua', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '1', 'Last Name': 'Gibson', 'Fri': '1', 'Tue': '1', 'Thu': '1', 'First Name': 'Rosemary', 'Mon': '1'}, {'Category': 'Medicine', 'Wed': '1', 'Last Name': 'Headrick', 'Fri': '1', 'Tue': '1', 'Thu': '1', 'First Name': 'Linda', 'Mon': '1'}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Hirsh', 'Fri': '1', 'Tue': '', 'Thu': '', 'First Name': 'David', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Holmboe', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Eric', 'Mon': '1'}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Huntington', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Jonathan', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '1', 'Last Name': 'Johnson', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Julie', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Kirkland', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Kathy', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Lannon', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Carole', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Lewin', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Linda', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '1', 'Last Name': 'Lypson', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Monica', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Madigosky', 'Fri': '', 'Tue': '1', 'Thu': '', 'First Name': 'Wendy', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Mahaniah', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Kiame', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Ogrinc', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Greg', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Satish', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Usha', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Shalaby', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Marc', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Stevenson', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Katherine', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Suresh', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Gautham', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Th_rne', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Karin', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Thor', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Johan', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Viggiano', 'Fri': '', 'Tue': '', 'Thu': '1', 'First Name': 'Thomas', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Warm', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Eric', 'Mon': ''}, {'Category': 'Medicine', 'Wed': '', 'Last Name': 'Watson', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Kathleen', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Altmiller', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Gerry', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '1', 'Last Name': 'Armstrong', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Gail', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Beel-Bates', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Cindy', 'Mon': '1'}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Dolansky', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Mary', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Durham', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Carol', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Duthie', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Beth', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Georges', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Alicia', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Goodman', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Daisy', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Groves', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Patricia', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Hill', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Connie', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Miltner', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Suzie', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Mitchell', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': ' Pam', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Moore', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Shirley', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Mueller', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Christine', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Reeves', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Susan', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '1', 'Last Name': 'Robertson', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Bethany', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Thompson', 'Fri': '', 'Tue': '1', 'Thu': '', 'First Name': 'Sarah', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Tilden', 'Fri': '', 'Tue': '', 'Thu': '1', 'First Name': 'Ginny', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Wakefield', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Bonnie ', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Yannaco', 'Fri': '', 'Tue': '', 'Thu': '', 'First Name': 'Terri', 'Mon': ''}, {'Category': 'Nursing', 'Wed': '', 'Last Name': 'Zierler', 'Fri': '1', 'Tue': '', 'Thu': '', 'First Name': 'Brenda', 'Mon': ''}]
                                     ,
                                     ['Health Administration', 'Medicine', 'Nursing'])


class TablesFixture(object):
    """This fixture represents data imported using import_tables()"""
    def __init__(self, l):
        self.tables = l


big_tables_fixture = TablesFixture([{'Wed': '7', 'Fri': '5', 'Thu': '5',
                                     'Mon': '5', 'Table Name': 'Head',
                                     'Tue': '5'},
                                    {'Wed': '7', 'Fri': '7', 'Thu': '7',
                                     'Mon': '7', 'Table Name': '2',
                                     'Tue': '7'},
                                    {'Wed': '7', 'Fri': '7', 'Thu': '7',
                                     'Mon': '7', 'Table Name': '3',
                                     'Tue': '7'},
                                    {'Wed': '7', 'Fri': '7', 'Thu': '7',
                                     'Mon': '7', 'Table Name': '4',
                                     'Tue': '7'},
                                    {'Wed': '7', 'Fri': '8', 'Thu': '8',
                                     'Mon': '8', 'Table Name': '5',
                                     'Tue': '8'},
                                    {'Wed': '7', 'Fri': '8', 'Thu': '8',
                                     'Mon': '8', 'Table Name': '6',
                                     'Tue': '8'},
                                    {'Wed': '8', 'Fri': '8', 'Thu': '8',
                                     'Mon': '8', 'Table Name': '7',
                                     'Tue': '8'},
                                    {'Wed': '8', 'Fri': '8', 'Thu': '8',
                                     'Mon': '8', 'Table Name': '8',
                                     'Tue': '8'},
                                    {'Wed': '8', 'Fri': '8', 'Thu': '8',
                                     'Mon': '8', 'Table Name': '9',
                                     'Tue': '8'},
                                    {'Wed': '8', 'Fri': '8', 'Thu': '8',
                                     'Mon': '8', 'Table Name': '10',
                                     'Tue': '8'}]
)

test_table = Table('4')
test_grouping = Grouping(test_table, 'Wed', '7')