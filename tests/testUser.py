from model.user import User
from unittest import TestCase
from schema import build_user, build_positions, build_trades

# to execute from the base of the project directory structure run:
# python3 -m unittest tests/testUser.py
# to run all tests in a directory run:
# python3 -m unittest tests discover

class TestUser(TestCase):

    def setUp(self):
        build_user()
        build_positions()
        build_trades()

        mike = User(**{
            "username": "mikebloom",
            "realname": "Mike Bloom",
            "balance": 10000.0
        })
        mike.hash_password("password")
        mike.generate_api_key()
        mike.save()
    
    def tearDown(self):
        pass
    
    def testFromPk(self):
        mike = User.from_pk(1)
        self.assertEqual(mike.realname, "Mike Bloom", 
            "Lookup from pk populates instance properties.")
    
    def testSavePk(self):
        # test that pk is defined after a save
        greg = User(**{
            "username": "gregcoin",
            "realname": "Greg Smith",
            "balance": 200.0,
            "password": "12345"
        })
        # greg.hash_password("12345")
        self.assertIsNone(greg.pk,
            "pk value of new instance initializes to None")
        
        greg.save()

        self.assertGreater(greg.pk, 1,
            "pk is set after first save")
    
    def testSaveUpdate(self):
        mike = User.from_pk(1)
        oldpk = mike.pk

        mike.balance = 0.0
        mike.save()

        self.assertEqual(mike.pk, oldpk,
            "pk does not change after save of existing row")
        
        mikeagain = User.from_pk(1)
        self.assertAlmostEqual(mikeagain.balance, 0.0,
            "updated properties saved to database and reloaded")
    
    def testOneWhere(self):
        mike = User.one_where("username=?", ('mikebloom',))

        self.assertIsNotNone(mike, "Query does not return None when row is found")
        self.assertEqual(mike.realname, "Mike Bloom", "Object returned has correct properties")
    
    def testManyWhere(self):
        mike = User.many_where("username=?", ('mikebloom',))
        self.assertIsInstance(mike, list, "many_where returns a list")
        self.assertEqual(len(mike), 1, "list is 1 element")
        self.assertEqual(mike[0].realname, "Mike Bloom", "many_where retrieves correct data")

    def testAll(self):
        mike = User.all()
        self.assertIsInstance(mike, list, "all returns a list")
        self.assertEqual(len(mike), 1, "list is 1 element")
        self.assertEqual(mike[0].realname, "Mike Bloom", "all retrieves correct data")

    def testDelete(self):
        mike = User.from_pk(1)
        mike.delete()
        self.assertIsNone(mike.pk, ".delete should set pk to None")
        secondmike = User.from_pk(1)
        self.assertIsNone(secondmike, ".delete removes row from db")

    def testLogin(self):
        notauser = User.login("carter", "notmypassword")
        self.assertIsNone(notauser, "bad credentials return the None object")

        mike = User.login("mikebloom", "password")
        self.assertEqual(mike.realname, "Mike Bloom", "good credentials retrieve User object")
    
    def testBuyNoMoney(self):
        mike = User.from_pk(1)
        with self.assertRaises(ValueError, msg="Should raise Value Error for negative amount"):
            mike.buy('stok', -1)
    '''
    def testRichest(self):
        mike = User.richest()
        self.assertEqual(mike.realname,"Mike Bloom", "richest function should return the richest user")
        jack = User(**{
            "username": "jackcoin",
            "realname": "Jack Smith",
            "balance": 10000000.0,
            "password": "12345"
        })
        jack.save()
        new_richest = User.richest()
        self.assertEqual(new_richest.realname,"Ahad Badruddin", "richest function should return the richest user")

'''
    def testApiKey(self):
        john = User(**{
            "username": "johnsmith",
            "realname": "John Smith",
            "balance": 200.0,
            "password": "12345"
        })
        john.generate_api_key()
        original_api_key= john.api_key
        john.save()
        reloaded_john = User.one_where("username=?", ('johnsmith',))
        self.assertEqual(original_api_key,reloaded_john.api_key, "api key is the same when it is created and reloaded")

    def testApiKeyAuth(self):
        mike = User.from_pk(1)
        mike_from_api_key = User.api_authenticate(mike.api_key)
        self.assertEqual(mike.realname,mike_from_api_key.realname,"got the same mike from two ways")
        jack = User.api_authenticate('0000000')
        self.assertIsNone(jack,"no user is found")