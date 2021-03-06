import unittest
from ddt import ddt, data, unpack
from provider.article_structure import ArticleInfo
import provider.article_structure as article_structure


@ddt
class TestArticleStructure(unittest.TestCase):

    @unpack
    @data({'input': 'elife-07702-vor-r4.zip', 'expected': None},
          {'input': 'elife-00013-vor-v1-20121015000000.zip', 'expected':'2012-10-15T00:00:00Z'})
    def test_get_update_date_from_zip_filename(self, input, expected):
        self.articleinfo = ArticleInfo(input)
        result = self.articleinfo.get_update_date_from_zip_filename()
        self.assertEqual(result, expected)

    @unpack
    @data({'input': 'elife-07702-vor-r4.zip', 'expected': None},
          {'input': 'elife-00013-vor-v1-20121015000000.zip', 'expected': '1'})
    def test_get_version_from_zip_filename(self, input, expected):
        self.articleinfo = ArticleInfo(input)
        result = self.articleinfo.get_version_from_zip_filename()
        self.assertEqual(result, expected)

    @unpack
    @data(
        {'input': 'elife-07702-vor-r4.zip', 'expected': 'ArticleZip'},
        {'input': 'elife-00013-vor-v1-20121015000000.zip', 'expected': 'ArticleZip'},
        {'input': 'elife-00666-v1.pdf', 'expected': 'Other'},
        {'input': 'elife-00666-v1.xml', 'expected': 'ArticleXML'},
        {'input': 'elife-00666-app1-fig1-v1.tif', 'expected': 'Figure'},
        {'input': 'elife-00666-app1-fig1-figsupp1-v1.tif', 'expected': 'Figure'},
        {'input': 'elife-00666-app2-video1.mp4', 'expected': 'Other'},
        {'input': 'elife-00666-box2-fig1-v1.tif', 'expected': 'Figure'},
        {'input': 'elife-00666-code1-v1.xml', 'expected': 'Other'},
        {'input': 'elife-00666-data1-v1.xlsx', 'expected': 'Other'},
        {'input': 'elife-00666-fig1-v1.tif', 'expected': 'Figure'},
        {'input': 'elife-00666-fig2-v1.tif', 'expected': 'Figure'},
        {'input': 'elife-00666-fig2-figsupp1-v1.tif', 'expected': 'Figure'},
        {'input': 'elife-00666-fig2-figsupp2-v1.tif', 'expected': 'Figure'},
        {'input': 'elife-00666-fig3-v1.tif', 'expected': 'Figure'},
        {'input': 'elife-00666-fig3-v10.tif', 'expected': 'Figure'},
        {'input': 'elife-00666-fig3-figsupp1-v1.tif', 'expected': 'Figure'},
        {'input': 'elife-00666-fig3-video1.mp4', 'expected': 'Other'},
        {'input': 'elife-00666-fig4-v1.tif', 'expected': 'Figure'},
        {'input': 'elife-00666-fig4-code1-v1.xlsx', 'expected': 'Other'},
        {'input': 'elife-00666-figures-v1.pdf', 'expected': 'FigurePDF'},
        {'input': 'elife-00666-inf001-v1.jpeg', 'expected': 'Inline'},
        {'input': 'elife-00666-repstand1-v1.pdf', 'expected': 'Other'},
        {'input': 'elife-00666-resp-fig1-v1.png', 'expected': 'Figure'},
        {'input': 'elife-00666-resp-video1.mp4', 'expected': 'Other'},
        {'input': 'elife-00666-supp1-v1.csv', 'expected': 'Other'},
        {'input': 'elife-00666-supp2-v2.tif', 'expected': 'Other'},
        {'input': 'elife-00666-supp2-v3.docx', 'expected': 'Other'},
        {'input': 'elife-00666-table3-data1-v1.xlsx', 'expected': 'Other'},
        {'input': 'elife-00666-video1.mp4', 'expected': 'Other'},
        {'input': 'elife-00666-video1-data1-v1.xlsx', 'expected': 'Other'},
          )
    def test_get_file_type_from_zip_filename(self, input, expected):
        self.articleinfo = ArticleInfo(input)
        result = self.articleinfo.file_type
        self.assertEqual(result, expected)

    @unpack
    @data(
        {'input': 'elife-07702-vor-r4.zip', 'expected': False},
        {'input': 'elife-00013-vor-v1-20121015000000.zip', 'expected': False},
        {'input': 'elife-00666-v1.pdf', 'expected': False},
        {'input': 'elife-00666-v1.xml', 'expected': False},
        {'input': 'elife-00666-app1-fig1-v1.tif', 'expected': True},
        {'input': 'elife-00666-app1-fig1-figsupp1-v1.tif', 'expected': True},
        {'input': 'elife-00666-app2-video1.mp4', 'expected': False},
        {'input': 'elife-00666-box2-fig1-v1.tif', 'expected': True},
        {'input': 'elife-00666-code1-v1.xml', 'expected': False},
        {'input': 'elife-00666-data1-v1.xlsx', 'expected': False},
        {'input': 'elife-00666-fig1-v1.tif', 'expected': True},
        {'input': 'elife-00666-fig2-v1.tif', 'expected': True},
        {'input': 'elife-00666-fig2-figsupp1-v1.tif', 'expected': True},
        {'input': 'elife-00666-fig2-figsupp2-v1.tif', 'expected': True},
        {'input': 'elife-00666-fig3-v1.tif', 'expected': True},
        {'input': 'elife-00666-fig3-figsupp1-v1.tif', 'expected': True},
        {'input': 'elife-00666-fig3-video1.mp4', 'expected': False},
        {'input': 'elife-00666-fig4-v1.tif', 'expected': True},
        {'input': 'elife-00666-fig4-code1-v1.xlsx', 'expected': False},
        {'input': 'elife-00666-figures-v1.pdf', 'expected': False},
        {'input': 'elife-00666-inf001-v1.jpeg', 'expected': False},
        {'input': 'elife-00666-repstand1-v1.pdf', 'expected': False},
        {'input': 'elife-00666-resp-fig1-v1.png', 'expected': True},
        {'input': 'elife-00666-resp-video1.mp4', 'expected': False},
        {'input': 'elife-00666-supp1-v1.csv', 'expected': False},
        {'input': 'elife-00666-table3-data1-v1.xlsx', 'expected': False},
        {'input': 'elife-00666-video1.mp4', 'expected': False},
        {'input': 'elife-00666-video1-data1-v1.xlsx', 'expected': False},
        {'input': 'elife-00666-supp1-v1.tif', 'expected': False}
          )
    def test_article_figure(self, input, expected):
        self.assertEqual(article_structure.article_figure(input), expected)

    def test_get_original_files(self):
        files = ['elife-00666-fig2-figsupp2-v1.tif',
                 'elife-00666-fig2-figsupp2-v10.tif',
                 'elife-00666-inf001-v1.jpg',
                 'elife-00666-inf001-v1-80w.jpg',
                 'elife-00666-table3-data1-v1.xlsx',
                 'elife-07702-vor-r4.zip',
                 'elife-07398-media1.jpg']
        expected = ['elife-00666-fig2-figsupp2-v1.tif',
                    'elife-00666-fig2-figsupp2-v10.tif',
                    'elife-00666-inf001-v1.jpg',
                    'elife-00666-table3-data1-v1.xlsx']

        self.assertListEqual(article_structure.get_original_files(files), expected)

    def test_get_media_file_images(self):
        files = ['elife-00666-fig2-figsupp2-v1.tif',
                 'elife-00666-inf001-v1.jpg',
                 'elife-00666-inf001-v1-80w.jpg',
                 'elife-00666-table3-data1-v1.xlsx',
                 'elife-07702-vor-r4.zip',
                 'elife-00666-video2.jpg',
                 'elife-07398-media1.jpg']
        expected = ['elife-00666-video2.jpg',
                    'elife-07398-media1.jpg']
        self.assertListEqual(article_structure.get_media_file_images(files), expected)

    def test_get_figures_for_iiif(self):
        "Only .tif of original figures"
        files = ['elife-00666-app1-fig1-figsupp1-v1.tif',
                 'elife-00666-fig2-figsupp2-v1.tif',
                 'elife-00666-fig2-figsupp2-v1.jpg',
                 'elife-00666-inf001-v1.jpg',
                 'elife-00666-inf001-v1-80w.jpg',
                 'elife-00666-table3-data1-v1.xlsx',
                 'elife-07702-vor-r4.zip',
                 'elife-6148691793723703318-fig10-v1.gif',
                 'elife-9204580859652100230-fig2-data1-v1.xls',
                 'elife-00666-video2.jpg',
                 'elife-07398-media1.jpg']
        expected = ['elife-00666-app1-fig1-figsupp1-v1.tif',
                    'elife-00666-fig2-figsupp2-v1.tif',
                    'elife-00666-video2.jpg',
                    'elife-07398-media1.jpg']
        self.assertListEqual(article_structure.get_figures_for_iiif(files), expected)

    # see https://github.com/elifesciences/elife-continuum-documentation/blob/master/file-naming/file_naming_spec.md
    def test_get_figures_pdfs(self):
        files = ['elife-07398-media1.jpg',
                 'elife-00666-figures-v1.pdf',
                 'elife-00353-v1.pdf',
                 'elife-00353-v1.xml',
                 'elife-18425-figures-v2.pdf']
        expected = ['elife-00666-figures-v1.pdf',
                    'elife-18425-figures-v2.pdf']
        self.assertListEqual(article_structure.get_figures_pdfs(files), expected)


    @data(u'elife-15224-fig1-figsupp1.tif',
          u'elife-15224-resp-fig1.tif', u'elife-15224-figures.pdf',
          u'elife-15802-fig9-data3.docx', u'elife-11792.mp4',
          u'elife-00005-media1-code1.wrl')
    def test_is_video_file_false(self, filename):
        result = article_structure.is_video_file(filename)
        self.assertFalse(result)

    @data(u'elife-11792-media2.mp4', u'elife-15224-fig1-figsupp1-media.tif', u'elife-11792-video1.mp4',
          u'elife-99999-resp-media1.avi', u'elife-00005-media1.mov')
    def test_is_video_file_true(self,filename):
        result = article_structure.is_video_file(filename)
        self.assertTrue(result)

    @data(u'elife-15224-fig1-figsupp1.tif')
    def test_file_parts(self, filename):
        prefix, extension = article_structure.file_parts(filename)
        self.assertEqual(prefix, u'elife-15224-fig1-figsupp1')
        self.assertEqual(extension, u'tif')

    def test_get_videos(self):
        files = [u'elife-13273-fig1-v1.tif', u'elife-13273-fig2-figsupp1-v1.tif', u'elife-13273-fig2-figsupp2-v1.tif', u'elife-13273-fig2-figsupp3-v1.tif', u'elife-13273-fig2-v1.tif', u'elife-13273-fig3-data1-v1.xlsx', u'elife-13273-fig3-figsupp1-v1.tif', u'elife-13273-fig3-figsupp2-v1.tif', u'elife-13273-fig3-figsupp3-v1.tif', u'elife-13273-fig3-figsupp4-v1.tif', u'elife-13273-fig3-figsupp5-v1.tif', u'elife-13273-fig3-v1.tif', u'elife-13273-fig4-figsupp1-v1.tif', u'elife-13273-fig4-v1.tif', u'elife-13273-fig5-data1-v1.xlsx', u'elife-13273-fig5-figsupp1-v1.tif', u'elife-13273-fig5-v1.tif', u'elife-13273-fig6-data1-v1.xlsx', u'elife-13273-fig6-data2-v1.xlsx', u'elife-13273-fig6-figsupp1-v1.tif', u'elife-13273-fig6-figsupp2-v1.tif', u'elife-13273-fig6-v1.tif', u'elife-13273-fig7-v1.tif', u'elife-13273-fig8-v1.tif', u'elife-13273-fig9-v1.tif', u'elife-13273-figures-v1.pdf', u'elife-13273-media1.mp4', u'elife-13273-v1.pdf', u'elife-13273-v1.xml']

        result = article_structure.get_videos(files)

        self.assertListEqual(result, [u'elife-13273-media1.mp4'])

    def test_pre_ingest_assets(self):
        files = ['elife-00666-app1-fig1-figsupp1-v1.tif',
                 'elife-00666-fig2-figsupp2-v1.tif',
                 'elife-00666-fig2-figsupp2-v1.jpg',
                 'elife-00666-inf001-v1.jpg',
                 'elife-00666-inf001-v1-80w.jpg',
                 'elife-00666-table3-data1-v1.xlsx',
                 'elife-07702-vor-r4.zip',
                 'elife-6148691793723703318-fig10-v1.gif',
                 'elife-9204580859652100230-fig2-data1-v1.xls',
                 'elife-00666-video2.jpg',
                 'elife-07398-media1.jpg',
                 'elife-00666-figures-v1.pdf',
                 'elife-18425-figures-v2.pdf',
                 'elife-13273-media1.mp4']
        expected = ['elife-00666-app1-fig1-figsupp1-v1.tif',
                    'elife-00666-fig2-figsupp2-v1.tif',
                    'elife-00666-video2.jpg',
                    'elife-07398-media1.jpg',
                    'elife-13273-media1.mp4',
                    'elife-00666-figures-v1.pdf',
                    'elife-18425-figures-v2.pdf']
        self.assertItemsEqual(article_structure.pre_ingest_assets(files), expected)

if __name__ == '__main__':
    unittest.main()
