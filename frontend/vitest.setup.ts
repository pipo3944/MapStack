import '@testing-library/react';
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';

// DOMをクリーンアップする
afterEach(() => {
  cleanup();
});

// テスト用にグローバル設定を拡張
// これにより、より直感的なテストが書けるようになります
expect.extend({
  // カスタムマッチャーを追加できます
}); 