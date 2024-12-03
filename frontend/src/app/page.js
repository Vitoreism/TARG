import {League_Spartan} from "next/font/google";

const leagueSpartan = League_Spartan({ subsets: ["latin"], weight: ["400", "700"] });

export default function HomePage() {
  return (
    <div>
      {/* Primeira seção com a imagem de fundo */}
      <section
        className={`relative bg-cover bg-center flex items-center text-white ${leagueSpartan.className}`}
        style={{
          backgroundImage: "url('/background_home_page.jpg')",
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
          minHeight: "92vh", // Garante que a imagem ocupe toda a altura da tela
        }}
      >
        <div className="absolute inset-0 bg-black bg-opacity-50"></div> {/* Sobreposição escura */}
        
        <div className="relative z-10 flex items-center max-w-7xl mx-auto px-6 py-32">
          <div className="max-w-lg mr-96">
            <h1 className="text-6xl font-bold mb-4 whitespace-nowrap">Transforme Notícias Em Lucro</h1>
            <h2 className="text-4xl font-medium mb-6">invista com inteligência</h2>
            <p className="text-lg">
              Utilize o poder da inteligência artificial para ir além das especulações.
              Nossa plataforma analisa grandes volumes de notícias, detectando sinais
              de mudança no mercado para fornecer previsões confiáveis, garantindo que
              suas estratégias sejam sempre bem fundamentadas.
            </p>
          </div>

          <div className="relative z-10 ml-auto">
            <img src="/just_image.png" alt="Logo" className="h-48" />
          </div>
        </div>
      </section>

      {/* Conteúdo adicional que rola abaixo da primeira seção */}
      <section className="bg-gray-100 py-16">
        <div className="max-w-5xl mx-auto px-6">
          <h2 className="text-3xl font-semibold mb-6">Continue explorando...</h2>
          <p className="text-lg mb-6">
            A plataforma oferece várias ferramentas poderosas para ajudar você a tomar decisões de investimento baseadas em dados reais.
          </p>
          {/* Mais conteúdo aqui */}
        </div>
      </section>

      {/* Outras seções de conteúdo */}
      <section className="bg-white py-16">
        <div className="max-w-5xl mx-auto px-6">
          <h2 className="text-3xl font-semibold mb-6">Nosso impacto</h2>
          <p className="text-lg mb-6">
            Ao usar nossa plataforma, você terá uma visão mais precisa sobre as mudanças no mercado e como elas podem impactar seus investimentos.
          </p>
        </div>
      </section>
    </div>
  );
}