export default function NewsPage() {
    return (
      <section className="p-4">
        <h1 className="text-3xl font-bold">Financial News</h1>
        <ul className="mt-4">
          <li className="border-b py-2">
            <a href="#" className="text-blue-600 hover:underline">
              Market rallies after tech earnings beat expectations
            </a>
          </li>
          <li className="border-b py-2">
            <a href="#" className="text-blue-600 hover:underline">
              Global oil prices reach a new high for the year
            </a>
          </li>
        </ul>
      </section>
    );
  }