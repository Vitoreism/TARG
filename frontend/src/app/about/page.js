export default function About() {
  return (
    <div className="bg-gray-900 text-white p-6 min-h-screen flex flex-col">
      {/* Seção de Introdução */}
      <section className="bg-gradient-to-r from-purple-600 to-blue-800 text-center py-12 rounded-lg mb-8">
        <h1 className="text-4xl font-bold mb-4">Sobre a TARG</h1>
        <p className="text-xl">
          A TARG é uma plataforma projetada para ajudar investidores com pouco tempo, fornecendo previsões
          baseadas em Inteligência Artificial (IA) e no Processamento de Linguagem Natural (NLP) de notícias
          sobre o mercado financeiro.
        </p>
      </section>

      {/* Seção de Missão */}
      <section className="bg-gray-800 py-8 px-6 rounded-lg mb-8">
        <h2 className="text-3xl text-purple-600 mb-4">Missão</h2>
        <p className="text-lg">
          Nossa missão é tornar as decisões de investimento mais rápidas e informadas, aproveitando ao máximo as 
          notícias financeiras.
        </p>
      </section>

      {/* Seção de GitHub */}
      <section className="bg-gray-800 py-8 px-6 rounded-lg mb-8">
        <h2 className="text-3xl text-purple-600 mb-4">Projeto no GitHub</h2>
        <p className="text-lg mb-4">
          Confira o código-fonte do nosso projeto e veja como estamos utilizando IA e NLP para ajudar investidores. Contribua e ajude-nos a evoluir!
        </p>
        <a
          href="https://github.com/Vitoreism/TARG"
          target="_blank"
          rel="noopener noreferrer"
          className="bg-gradient-to-r from-purple-600 to-blue-800 text-white py-2 px-6 rounded-lg hover:opacity-80 transition"
        >
          Acesse o GitHub
        </a>
      </section>

      {/* Seção de Integrantes */}
      <section className="bg-gray-800 py-8 px-6 rounded-lg">
        <h2 className="text-3xl text-purple-600 mb-4">Integrantes do Projeto</h2>
        <p className="text-lg mb-4">
          A TARG é um projeto de hackathon do TRIL Lab desenvolvido pelos estudantes do curso de
          ciência da computação da UFPB:
        </p>
        <ul className="list-disc pl-6 text-lg">
          <li>Davi Gurgel</li>
          <li>Rafael Torres</li>
          <li>Vitor Reis</li>
          <li>Marcus Araujo</li>
        </ul>
      </section>
    </div>
  );
}
