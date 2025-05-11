import {
    useCreateDocumentApiV1DocumentsPost,
    useGetDocumentApiV1DocumentsDocumentIdGet,
    useGetDocumentContentApiV1DocumentsDocumentIdContentGet,
    useGetDocumentDiffApiV1DocumentsDocumentIdDiffGet,
    useGetDocumentRevisionsApiV1DocumentsDocumentIdRevisionsGet,
    useGetDocumentsApiV1DocumentsGet,
    useGetDocumentVersionContentApiV1DocumentsDocumentIdContentVersionVersionGet,
    useUpdateDocumentApiV1DocumentsDocumentIdPut,
} from '@/api/generated/documents/documents';
import {
    DocumentCreate,
    DocumentRevisionCreate,
    GetDocumentDiffApiV1DocumentsDocumentIdDiffGetParams,
    GetDocumentsApiV1DocumentsGetParams
} from '@/api/model';
import { useState } from 'react';

/**
 * ドキュメント関連のAPIを呼び出すためのカスタムフック
 */
export const useDocuments = () => {
  const [searchParams, setSearchParams] = useState<GetDocumentsApiV1DocumentsGetParams>({
    page: 1,
    limit: 10,
  });

  // ドキュメント一覧を取得
  const documentsQuery = useGetDocumentsApiV1DocumentsGet(searchParams, {
    query: {
      staleTime: 1000 * 60 * 5, // 5分間キャッシュ
    },
  });

  // ドキュメント詳細を取得
  const getDocument = (documentId: string) => {
    return useGetDocumentApiV1DocumentsDocumentIdGet(documentId, {
      query: {
        staleTime: 1000 * 60 * 5, // 5分間キャッシュ
      },
    });
  };

  // ドキュメントの最新コンテンツを取得
  const getDocumentContent = (documentId: string) => {
    return useGetDocumentContentApiV1DocumentsDocumentIdContentGet(documentId, {
      query: {
        staleTime: 1000 * 60 * 5, // 5分間キャッシュ
      },
    });
  };

  // 特定バージョンのドキュメントコンテンツを取得
  const getDocumentVersionContent = (documentId: string, version: string) => {
    return useGetDocumentVersionContentApiV1DocumentsDocumentIdContentVersionVersionGet(
      documentId,
      version,
      {
        query: {
          staleTime: 1000 * 60 * 5, // 5分間キャッシュ
        },
      }
    );
  };

  // ドキュメントのリビジョン履歴を取得
  const getDocumentRevisions = (documentId: string) => {
    return useGetDocumentRevisionsApiV1DocumentsDocumentIdRevisionsGet(documentId, {
      query: {
        staleTime: 1000 * 60 * 5, // 5分間キャッシュ
      },
    });
  };

  // ドキュメントの差分を取得
  const getDocumentDiff = (documentId: string, params: GetDocumentDiffApiV1DocumentsDocumentIdDiffGetParams) => {
    return useGetDocumentDiffApiV1DocumentsDocumentIdDiffGet(documentId, params, {
      query: {
        staleTime: 1000 * 60 * 5, // 5分間キャッシュ
      },
    });
  };

  // 新規ドキュメントを作成
  const createDocumentMutation = useCreateDocumentApiV1DocumentsPost();

  // ドキュメントを更新
  const updateDocumentMutation = useUpdateDocumentApiV1DocumentsDocumentIdPut();

  // 新規ドキュメントを作成する関数
  const createDocument = async (document: DocumentCreate) => {
    try {
      const result = await createDocumentMutation.mutateAsync({ data: document });
      return { success: true, data: result };
    } catch (error) {
      console.error('Failed to create document:', error);
      return { success: false, error };
    }
  };

  // ドキュメントを更新する関数
  const updateDocument = async (documentId: string, document: DocumentRevisionCreate) => {
    try {
      const result = await updateDocumentMutation.mutateAsync({
        documentId,
        data: document,
      });
      return { success: true, data: result };
    } catch (error) {
      console.error('Failed to update document:', error);
      return { success: false, error };
    }
  };

  // 検索パラメータを更新する関数
  const updateSearchParams = (newParams: Partial<GetDocumentsApiV1DocumentsGetParams>) => {
    setSearchParams((prev) => ({ ...prev, ...newParams }));
  };

  return {
    // クエリ
    documentsQuery,
    getDocument,
    getDocumentContent,
    getDocumentVersionContent,
    getDocumentRevisions,
    getDocumentDiff,

    // ミューテーション
    createDocument,
    updateDocument,

    // 状態
    searchParams,
    updateSearchParams,

    // ローディング状態
    isLoadingDocuments: documentsQuery.isLoading,
    isCreatingDocument: createDocumentMutation.isPending,
    isUpdatingDocument: updateDocumentMutation.isPending,
  };
};

export default useDocuments;
