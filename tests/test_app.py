import pytest
from app_gerenciamento import app_servicos
from flask_testing import TestCase

# Teste de integração da aplicação
class TestApp(TestCase):
    # Configuração de teste
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Usando um banco de dados separado para testes
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        """Configura o banco de dados para cada teste"""
        db.create_all()

    def tearDown(self):
        """Limpa o banco de dados após cada teste"""
        db.session.remove()
        db.drop_all()

    def test_home_page(self):
        """Teste para a rota inicial"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('home', response.data.decode('utf-8'))

    def test_cliente_cadastro(self):
        """Teste de cadastro de cliente"""
        with self.client:
            response = self.client.post('/cad_cliente', data=dict(
                nome='Cliente Teste',
                telefone='12345678901',
                email='cliente@teste.com',
                endereco='Rua Teste, 123'
            ), follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('Cliente cadastrado com sucesso!', response.data.decode('utf-8'))

    def test_servico_cadastro(self):
        """Teste de cadastro de serviço"""
        with self.client:
            response = self.client.post('/servicos', data=dict(
                descricao='Serviço Teste',
                preco='100',
                duracao='1 hora'
            ), follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('serviço cadastrado com sucesso!', response.data.decode('utf-8'))

    def test_login(self):
        """Teste de login"""
        # Cria um usuário para teste
        user = Usu(usuario="usuario_teste", email="teste@teste.com", senha="1234")
        user.senhacrip = "1234"  # Criptografa a senha
        db.session.add(user)
        db.session.commit()

        with self.client:
            response = self.client.post('/login', data=dict(
                usuario='usuario_teste',
                senha='1234'
            ), follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('login realizado com sucesso', response.data.decode('utf-8'))