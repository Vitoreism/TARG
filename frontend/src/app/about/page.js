export default function AboutPage() {
  return (
    <section className="p-4">
      <h1 className="text-4xl font-bold mb-6">Sobre a TARG</h1>
      <p className="text-lg mb-4">
        A TARG é um projeto inovador desenvolvido durante o hackathon do TRIL Lab com o objetivo de revolucionar a forma como as pessoas investem. Utilizando as mais recentes tecnologias em inteligência artificial, a TARG analisa vastos volumes de dados do mercado financeiro para fornecer previsões precisas e insights valiosos para seus usuários.
      </p>
      <h2 className="text-2xl font-semibold mb-4">Nossas Tecnologias</h2>
      <ul className="list-disc list-inside">
        <li>Inteligência Artificial</li>
        <li>Machine Learning</li>
        <li>Processamento de Linguagem Natural (NLP)</li>
        <li>Análise de Dados</li>
      </ul>
      <h2 className="text-2xl font-semibold mb-4">Nossa Missão</h2>
      <p className="text-lg">
        Nossa missão é democratizar o acesso a informações financeiras e ferramentas de investimento de alta qualidade, permitindo que qualquer pessoa possa tomar decisões mais inteligentes e alcançar seus objetivos financeiros.
      </p>
    </section>
  );
}