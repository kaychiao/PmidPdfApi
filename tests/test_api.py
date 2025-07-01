import unittest
from app import create_app
from models import db, Article
import json
import os
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    PDF_ROOT_PATH = "/tmp/test_pdfs"

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test directory
        os.makedirs(TestConfig.PDF_ROOT_PATH, exist_ok=True)
        
        # Add a test article
        test_article = Article(
            pmid="12345",
            doi="10.1234/test",
            title="Test Article",
            authors="Test Author",
            journal="Test Journal",
            year=2023,
            has_pdf=True,
            has_abstract=True,
            full_text_available=True,
            commercial_use_allowed=False,
            relative_path="123/45",
            download_attempted=True
        )
        db.session.add(test_article)
        db.session.commit()
        
        # Create test PDF file
        os.makedirs(os.path.join(TestConfig.PDF_ROOT_PATH, "123/45"), exist_ok=True)
        with open(os.path.join(TestConfig.PDF_ROOT_PATH, "123/45", "article.pdf"), "w") as f:
            f.write("Test PDF content")
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
        # Clean up test directory
        import shutil
        if os.path.exists(TestConfig.PDF_ROOT_PATH):
            shutil.rmtree(TestConfig.PDF_ROOT_PATH)
    
    def test_health_check(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_get_pdf_existing(self):
        response = self.client.get('/api/pdf/12345', headers={'X-API-Key': 'test-key'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['pmid'], '12345')
        self.assertIn('pdf_url', data)
    
    def test_get_pdf_not_found(self):
        response = self.client.get('/api/pdf/99999', headers={'X-API-Key': 'test-key'})
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['code'], 'PDF_NOT_AVAILABLE')
    
    def test_invalid_api_key(self):
        response = self.client.get('/api/pdf/12345', headers={'X-API-Key': 'invalid-key'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['code'], 'AUTH_ERROR')

if __name__ == '__main__':
    unittest.main()