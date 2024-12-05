'use client';

import { useEffect, useState } from "react";
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { League_Spartan } from "next/font/google";

// Registra os componentes necessários do Chart.js
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const leagueSpartan = League_Spartan({ subsets: ["latin"], weight: ["400", "700"] });

export default function HomePage() {
  const [chartData, setChartData] = useState(null); // Estado para os dados do gráfico
  const [loading, setLoading] = useState(true); // Estado de carregamento
  const [error, setError] = useState(null); // Estado de erro

  useEffect(() => {
    // Função para buscar os dados da API
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/stock'); // Supondo que sua API esteja rodando no localhost na porta 8000
        const data = await response.json();

        // Formatação dos dados para o gráfico
        const labels = [data.date]; // Usando a data como label (você pode melhorar isso)
        const values = [data.price]; // Aqui pegamos o preço, mas você pode adicionar mais dados, como RSI ou MACD

        setChartData({
          labels: labels,
          datasets: [
            {
              label: 'Preço da Ação',
              data: values,
              borderColor: 'rgba(75, 192, 192, 1)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              fill: true,
            },
          ],
        });
        setLoading(false);
      } catch (error) {
        console.error('Erro ao buscar dados da API:', error);
        setError('Erro ao carregar os dados.');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="mt-48">Carregando gráfico...</div>;
  }
  
  if (error) {
    return <div>{error}</div>;
  }

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
          minHeight: "76vh",
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

      {/* Seção com o gráfico */}
      <section className="bg-white py-16">
        <div className="max-w-5xl mx-auto px-6">
          <h2 className="text-3xl font-semibold mb-6">Análise de Dados</h2>
          <p className="text-lg mb-6">
            Aqui estão as últimas tendências de mercado baseadas nas notícias analisadas.
          </p>
          {/* Renderiza o gráfico se os dados estiverem disponíveis */}
          {chartData && (
            <div style={{ width: '100%', height: '400px' }}>
              <Line data={chartData} />
            </div>
          )}
        </div>
      </section>

      {/* Outras seções de conteúdo */}
      <section className="bg-gray-100 py-16">
        <div className="max-w-5xl mx-auto px-6">
          <h2 className="text-3xl font-semibold mb-6">Continue explorando...</h2>
          <p className="text-lg mb-6">
            A plataforma oferece várias ferramentas poderosas para ajudar você a tomar decisões de investimento baseadas em dados reais.
          </p>
        </div>
      </section>
    </div>
  );
}
