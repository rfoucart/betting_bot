import pandas as pd
import datetime
from pandas.testing import assert_frame_equal
from tools.parsers import add_review_date, fix_combined_bets, merge_similar_bets


class TestReviewDate:
    def test_review_date_for_same_day_before_6am(self):
        data = {
            'Date': [datetime.datetime(2022, 1, 1, 5, 0)],
            'Value': [1]
        }
        df = pd.DataFrame(data)
        result = add_review_date(df)
        expected_data = {
            'Date': [datetime.datetime(2022, 1, 1, 5, 0)],
            'Value': [1],
            'ReviewDate': ['31/12/2021']
        }
        expected_df = pd.DataFrame(expected_data)
        assert_frame_equal(result, expected_df)

    def test_review_date_for_same_day_after_6am(self):
        data = {
            'Date': [datetime.datetime(2022, 1, 1, 7, 0)],
            'Value': [1]
        }
        df = pd.DataFrame(data)
        result = add_review_date(df)
        expected_data = {
            'Date': [datetime.datetime(2022, 1, 1, 7, 0)],
            'Value': [1],
            'ReviewDate': ['01/01/2022']
        }
        expected_df = pd.DataFrame(expected_data)
        assert_frame_equal(result, expected_df)

    def test_review_date_for_multiple_dates(self):
        data = {
            'Date': [datetime.datetime(2022, 1, 1, 5, 0), datetime.datetime(2022, 1, 1, 7, 0)],
            'Value': [1, 2]
        }
        df = pd.DataFrame(data)
        result = add_review_date(df)
        expected_data = {
            'Date': [datetime.datetime(2022, 1, 1, 5, 0), datetime.datetime(2022, 1, 1, 7, 0)],
            'Value': [1, 2],
            'ReviewDate': ['31/12/2021', '01/01/2022']
        }
        expected_df = pd.DataFrame(expected_data)
        assert_frame_equal(result, expected_df)


class TestFixCombinedBets:
    def test_fills_empty_fields_with_previous_value(self):
        data = {
            'Catégorie': ['boosts', None, 'values'],
            'Type': ['type1', 'type2', None]
        }
        df = pd.DataFrame(data)
        result = fix_combined_bets(df)
        expected_data = {
            'Catégorie': ['boosts', 'boosts', 'values'],
            'Type': ['type1', 'type2', 'type2']
        }
        expected_df = pd.DataFrame(expected_data)
        assert_frame_equal(result, expected_df)

    def test_leaves_non_empty_fields_unchanged(self):
        data = {
            'Catégorie': ['boosts', 'values', 'boosts'],
            'Type': ['type1', 'type2', 'type3']
        }
        df = pd.DataFrame(data)
        result = fix_combined_bets(df)
        expected_df = df.copy()
        assert_frame_equal(result, expected_df)

    def test_handles_all_empty_fields(self):
        data = {
            'Catégorie': [None, None, None],
            'Type': [None, None, None]
        }
        df = pd.DataFrame(data)
        result = fix_combined_bets(df)
        expected_df = df.copy()
        assert_frame_equal(result, expected_df)


class TestMergeSimilarBets:
    def test_merges_bets_with_same_name_cote_and_date(self):
        data = {
            'Intitulé du pari': ['bet1', 'bet1', 'bet2'],
            'Cote': [1.5, 1.5, 2.0],
            'Date': ['01/01/2022', '01/01/2022', '02/01/2022'],
            'Etat': ['Gagné', 'Gagné', 'Perdu'],
            'Mise': [10, 20, 30],
            'Gain': [15, 30, 0],
            'Bonus de gain': [0, 0, 0],
            'Commission': [0, 0, 0],
            'Bénéfice': [5, 10, -30],
            'Bookmaker': ['book1', 'book1', 'book2'],
            'Catégorie': ['cat1', 'cat1', 'cat2'],
            'Closing Odds': [1.5, 1.5, 2.0],
            'Commentaire': ['comment1', 'comment2', 'comment3'],
            'Compétition': ['comp1', 'comp1', 'comp2'],
            'Live': [False, False, True],
            'Pari gratuit': [False, True, False],
            'Sport': ['sport1', 'sport1', 'sport2'],
            'Tipster': ['tipster1', 'tipster1', 'tipster2'],
            'Type': ['type1', 'type1', 'type2'],
            'Type de pari': ['type1', 'type1', 'type2']
        }
        df = pd.DataFrame(data)
        result = merge_similar_bets(df)
        expected_data = {
            'Intitulé du pari': ['bet1', 'bet2'],
            'Cote': [1.5, 2.0],
            'Date': ['01/01/2022', '02/01/2022'],
            'Etat': ['Gagné', 'Perdu'],
            'Mise': [30, 30],
            'Gain': [45, 0],
            'Bonus de gain': [0, 0],
            'Commission': [0, 0],
            'Bénéfice': [15, -30],
            'Bookmaker': ['', ''],
            'Catégorie': ['cat1', 'cat2'],
            'Closing Odds': [1.5, 2.0],
            'Commentaire': ['comment1comment2', 'comment3'],
            'Compétition': ['comp1', 'comp2'],
            'Live': [False, True],
            'Pari gratuit': [False, False],
            'Sport': ['sport1', 'sport2'],
            'Tipster': ['tipster1', 'tipster2'],
            'Type': ['type1', 'type2'],
            'Type de pari': ['type1', 'type2']
        }
        expected_df = pd.DataFrame(expected_data)
        expected_df = expected_df.sort_index(axis=1)
        result = result.sort_index(axis=1)
        assert_frame_equal(result, expected_df)

    def test_leaves_bets_with_different_name_cote_or_date_unchanged(self):
        data = {
            'Intitulé du pari': ['bet1', 'bet1', 'bet2'],
            'Cote': [1.5, 2.0, 2.0],
            'Date': ['01/01/2022', '02/01/2022', '02/01/2022'],
            'Etat': ['Gagné', 'Gagné', 'Perdu'],
            'Mise': [10, 20, 30],
            'Gain': [15, 40, 0],
            'Bonus de gain': [0, 0, 0],
            'Commission': [0, 0, 0],
            'Bénéfice': [5, 20, -30],
            'Bookmaker': ['book1', 'book2', 'book2'],
            'Catégorie': ['cat1', 'cat1', 'cat2'],
            'Closing Odds': [1.5, 1.5, 2.0],
            'Commentaire': ['comment1', 'comment2', 'comment3'],
            'Compétition': ['comp1', 'comp1', 'comp2'],
            'Live': [False, False, True],
            'Pari gratuit': [False, True, False],
            'Sport': ['sport1', 'sport1', 'sport2'],
            'Tipster': ['tipster1', 'tipster1', 'tipster2'],
            'Type': ['type1', 'type1', 'type2'],
            'Type de pari': ['type1', 'type1', 'type2']
        }
        df = pd.DataFrame(data)
        result = merge_similar_bets(df)
        expected_data = {
            'Intitulé du pari': ['bet1', 'bet1', 'bet2'],
            'Cote': [1.5, 2.0, 2.0],
            'Date': ['01/01/2022', '02/01/2022', '02/01/2022'],
            'Etat': ['Gagné', 'Gagné', 'Perdu'],
            'Mise': [10, 20, 30],
            'Gain': [15, 40, 0],
            'Bonus de gain': [0, 0, 0],
            'Commission': [0, 0, 0],
            'Bénéfice': [5, 20, -30],
            'Bookmaker': ['', '', ''],
            'Catégorie': ['cat1', 'cat1', 'cat2'],
            'Closing Odds': [1.5, 1.5, 2.0],
            'Commentaire': ['comment1', 'comment2', 'comment3'],
            'Compétition': ['comp1', 'comp1', 'comp2'],
            'Live': [False, False, True],
            'Pari gratuit': [False, True, False],
            'Sport': ['sport1', 'sport1', 'sport2'],
            'Tipster': ['tipster1', 'tipster1', 'tipster2'],
            'Type': ['type1', 'type1', 'type2'],
            'Type de pari': ['type1', 'type1', 'type2']
        }
        expected_df = pd.DataFrame(expected_data)
        result = result.sort_index(axis=1)
        expected_df = expected_df.sort_index(axis=1)
        assert_frame_equal(result, expected_df)
