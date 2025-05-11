import { useGetNodeDocumentsApiV1NodesNodeIdDocumentsGet, useLinkNodeDocumentApiV1NodesNodeIdDocumentsPost, useUnlinkNodeDocumentApiV1NodesNodeIdDocumentsDocumentIdDelete } from '@/api/generated/nodes/nodes';
import { NodeDocumentLinkCreate } from '@/api/model';
import { isUuid } from '@/utils/nodeHandleMapping';

/**
 * ノードに関連付けられたドキュメントを操作するためのカスタムフック
 */
export const useNodeDocuments = () => {
  // ノードに関連付けられたドキュメントを取得
  const getNodeDocuments = (nodeId: string) => {
    // UUIDの場合は直接APIを呼び出す
    if (isUuid(nodeId)) {
      return useGetNodeDocumentsApiV1NodesNodeIdDocumentsGet(nodeId, {
        query: {
          staleTime: 1000 * 60 * 5, // 5分間キャッシュ
        },
      });
    }

    // ハンドル名の場合は、そのまま試してみる
    // 注：バックエンドで対応する必要があるかもしれません
    return useGetNodeDocumentsApiV1NodesNodeIdDocumentsGet(nodeId, {
      query: {
        staleTime: 1000 * 60 * 5, // 5分間キャッシュ
        retry: false, // エラー時の再試行なし
      },
    });
  };

  // ドキュメントをノードに関連付けるためのミューテーション
  const linkDocumentMutation = useLinkNodeDocumentApiV1NodesNodeIdDocumentsPost();

  // ドキュメントとノードの関連付けを解除するためのミューテーション
  const unlinkDocumentMutation = useUnlinkNodeDocumentApiV1NodesNodeIdDocumentsDocumentIdDelete();

  // ドキュメントをノードに関連付ける関数
  const linkDocument = async (nodeId: string, linkData: NodeDocumentLinkCreate) => {
    try {
      const result = await linkDocumentMutation.mutateAsync({
        nodeId,
        data: linkData,
      });
      return { success: true, data: result };
    } catch (error) {
      console.error('Failed to link document to node:', error);
      return { success: false, error };
    }
  };

  // ドキュメントとノードの関連付けを解除する関数
  const unlinkDocument = async (nodeId: string, documentId: string) => {
    try {
      const result = await unlinkDocumentMutation.mutateAsync({
        nodeId,
        documentId,
      });
      return { success: true, data: result };
    } catch (error) {
      console.error('Failed to unlink document from node:', error);
      return { success: false, error };
    }
  };

  return {
    // クエリ
    getNodeDocuments,

    // ミューテーション
    linkDocument,
    unlinkDocument,

    // ローディング状態
    isLinkingDocument: linkDocumentMutation.isPending,
    isUnlinkingDocument: unlinkDocumentMutation.isPending,
  };
};

export default useNodeDocuments;
