export default function Home() {
  return (
    <div className="bg-white w-full py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto text-center mb-16">
        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6">
          Welcome to <span className="text-blue-600">MapStack</span>
        </h1>

        <p className="text-xl sm:text-2xl mb-10">AIを活用した体系的な学習プラットフォーム</p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <a
            href="/roadmaps"
            className="p-6 border rounded-xl shadow-sm hover:shadow-md hover:border-blue-500 transition-all bg-white"
          >
            <h3 className="text-2xl font-bold mb-3">ロードマップ &rarr;</h3>
            <p className="text-lg text-gray-600">体系化された学習パスを見てみましょう</p>
          </a>

          <a
            href="/profile"
            className="p-6 border rounded-xl shadow-sm hover:shadow-md hover:border-blue-500 transition-all bg-white"
          >
            <h3 className="text-2xl font-bold mb-3">プロフィール &rarr;</h3>
            <p className="text-lg text-gray-600">あなたの学習進捗とプロフィールを確認</p>
          </a>

          <a
            href="/ai-assistant"
            className="p-6 border rounded-xl shadow-sm hover:shadow-md hover:border-blue-500 transition-all bg-white"
          >
            <h3 className="text-2xl font-bold mb-3">AIアシスタント &rarr;</h3>
            <p className="text-lg text-gray-600">AIによる個別最適化された学習体験</p>
          </a>

          <a
            href="/practice"
            className="p-6 border rounded-xl shadow-sm hover:shadow-md hover:border-blue-500 transition-all bg-white"
          >
            <h3 className="text-2xl font-bold mb-3">実践演習 &rarr;</h3>
            <p className="text-lg text-gray-600">実践的スキル獲得のための演習</p>
          </a>
        </div>
      </div>
    </div>
  );
}
