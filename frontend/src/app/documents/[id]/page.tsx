'use client';

import { DocumentRevisionContentResponse, DocumentRevisionResponse } from '@/api/model';
import { DocumentViewer, RevisionTimeline, VersionSelector } from '@/components/document';
import { useDocuments } from '@/hooks';
import { useEffect, useState } from 'react';

interface DocumentPageProps {
  params: {
    id: string;
  };
}

export default function DocumentPage({ params }: DocumentPageProps) {
  const { id } = params;
  const [selectedVersion, setSelectedVersion] = useState<string | null>(null);
  const [documentContent, setDocumentContent] = useState<DocumentRevisionContentResponse | null>(null);

  // APIフックを使用してデータを取得
  const { getDocument, getDocumentContent, getDocumentVersionContent, getDocumentRevisions } = useDocuments();
  const documentQuery = getDocument(id);
  const documentRevisionsQuery = getDocumentRevisions(id);
  const latestContentQuery = getDocumentContent(id);

  // 選択されたバージョンのコンテンツを取得
  const versionContentQuery = selectedVersion
    ? getDocumentVersionContent(id, selectedVersion)
    : null;

  // 初期化時と選択バージョン変更時にコンテンツを設定
  useEffect(() => {
    if (selectedVersion && versionContentQuery?.data) {
      setDocumentContent(versionContentQuery.data);
    } else if (!selectedVersion && latestContentQuery.data) {
      setDocumentContent(latestContentQuery.data);
    }
  }, [selectedVersion, versionContentQuery?.data, latestContentQuery.data]);

  // バージョン選択時の処理
  const handleVersionChange = (version: string) => {
    setSelectedVersion(version);
  };

  // タイムラインでバージョンがクリックされた時の処理
  const handleVersionClick = (version: string) => {
    setSelectedVersion(version);
  };

  // ローディング表示
  if (documentQuery.isLoading || latestContentQuery.isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // エラー表示
  if (documentQuery.isError || latestContentQuery.isError) {
    return (
      <div className="p-6 bg-red-50 text-red-700 rounded-md max-w-4xl mx-auto mt-8">
        <h2 className="text-xl font-bold mb-2">エラーが発生しました</h2>
        <p>{'ドキュメントの読み込みに失敗しました'}</p>
      </div>
    );
  }

  // ドキュメントが存在しない場合
  if (!documentQuery.data || !documentContent) {
    return (
      <div className="p-6 bg-yellow-50 text-yellow-700 rounded-md max-w-4xl mx-auto mt-8">
        <h2 className="text-xl font-bold mb-2">ドキュメントが見つかりません</h2>
        <p>指定されたIDのドキュメントは存在しないか、アクセス権限がありません。</p>
      </div>
    );
  }

  const document = documentQuery.data;
  // DocumentWithRevisionsResponseからrevisionsプロパティを取得し、配列であることを確認
  const revisions: DocumentRevisionResponse[] = documentRevisionsQuery.data?.revisions || [];

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">{document.title}</h1>
        {document.description && (
          <p className="text-gray-600 mb-4">{document.description}</p>
        )}
        <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500">
          <div>
            作成日: {new Date(document.created_at).toLocaleDateString()}
          </div>
          {document.updated_at && document.updated_at !== document.created_at && (
            <div>
              更新日: {new Date(document.updated_at).toLocaleDateString()}
            </div>
          )}
          <div>
            最終バージョン: {documentContent.version}
          </div>
        </div>
      </div>

      <div className="flex flex-col md:flex-row gap-8">
        <div className="w-full md:w-2/3">
          <div className="bg-white shadow-md rounded-lg p-6 mb-6">
            {/* バージョン選択UI */}
            {revisions.length > 0 && (
              <div className="mb-4">
                <VersionSelector
                  versions={revisions}
                  currentVersion={selectedVersion || documentContent.version}
                  onVersionChange={handleVersionChange}
                />
              </div>
            )}

            {/* ドキュメントビューアー */}
            <DocumentViewer document={documentContent.content} />
          </div>
        </div>

        <div className="w-full md:w-1/3">
          <div className="bg-white shadow-md rounded-lg p-6">
            {/* バージョン履歴タイムライン */}
            <RevisionTimeline
              documentId={id}
              revisions={revisions}
              currentVersion={selectedVersion || documentContent.version}
              onVersionClick={handleVersionClick}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
