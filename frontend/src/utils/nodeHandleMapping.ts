/**
 * ノードハンドル名とUUIDのマッピングを提供するユーティリティ
 *
 * 注：実際の実装では、このマッピングはAPIから取得するか、
 * グローバルステートに保存して管理するべきです。
 */

// 暫定的なダミーマッピング
// 注意: これらのUUIDは実際のデータベースに存在するものではなく、デモ目的で使用されています
// 実際の環境では、ノードのロード時にAPIから取得したデータを元に構築するか、
// バックエンドで対応するAPIを実装する必要があります
const handleToUuidMap: Record<string, string> = {
  // 注: 以下のIDは実際のデータベースに存在しないダミー値です
  'internet': '3a4e6c9d-8f1a-4b5e-9c3d-2e7f8a6b0c1d',
  'html': '5b7d9e2f-1c4a-8d3b-6e5f-9a7b8c1d2e3f',
  'css': '7e9d5b3a-2f1c-4a8d-3b6e-5f9a7b8c1d2e',
  'javascript': '9c7e5b3a-2f1c-4a8d-3b6e-5f9a7b8c1d2e',
  'how-internet-works': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
  'http': 'b2c3d4e5-f6a7-8901-bcde-f12345678901',
  // 他のハンドル名についても同様に定義
};

/**
 * ノードハンドル名からUUIDを取得する
 * @param handle ノードハンドル名
 * @returns UUID（見つからない場合はnull）
 */
export const getUuidFromHandle = (handle: string): string | null => {
  // 開発環境ではダミーのマッピングを返す
  // 本番環境では実際のマッピングを使用する
  if (process.env.NODE_ENV === 'development') {
    console.warn(`開発環境では実際のノードIDへのマッピングがないため、この機能は動作しません: ${handle}`);
    return null;
  }
  return handleToUuidMap[handle] || null;
};

/**
 * 文字列がUUID形式かどうかを判定する
 * @param str 判定する文字列
 * @returns UUID形式ならtrue、そうでなければfalse
 */
export const isUuid = (str: string): boolean => {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(str);
};
