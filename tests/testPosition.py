from model.user import User
from model.position import Position
from unittest import TestCase
from schema import build_user, build_positions

# to execute from the base of the project directory structure run:
# python3 -m unittest tests/testUser.py
# to run all tests in a directory run:
# python3 -m unittest tests discover

class TestPosition(TestCase):

    def setUp(self):
        build_user()
        build_positions()

        mike = User(**{
            "username": "mikebloom",
            "realname": "Mike Bloom",
            "balance": 10000.0
        })
        mike.hash_password("password")
        mike.save()

        aapl = Position(**{
            "ticker": "aapl",
            "amount": 5,
            "user_info_pk": mike.pk
        })
        tsla = Position(**{
            "ticker": "tsla",
            "amount": 10,
            "user_info_pk": mike.pk
        })
        aapl.save()
        tsla.save()
    
    def tearDown(self):
        pass
    
    def testDummy(self):
        pass
    
    def testOneWhere(self):
        # student exercise
        pass
    
    def testSave(self):
        # student exercise
        pass
    
    def testAllPositions(self):
        mike = User.from_pk(1)
        positions = mike.all_positions()
        self.assertIsInstance(positions, list, ".all_positions returns a list")
        firstposition = positions[0]
        self.assertIsInstance(firstposition, Position, "return is list of Positions")

    def testPosition(self):
        mike = User.from_pk(1)
        position = mike.position_for_stock("aapl")
        self.assertIsInstance(position, Position, "pfs returns Position object")