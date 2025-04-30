"""
ドキュメントサービスのテスト

このモジュールでは、ドキュメントサービスの主要機能をテストします。
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock

# コンテナ内のパスに合わせて修正
from src.services.document import VersionUtility, DocumentDiffUtility, DocumentService


class TestVersionUtility:
    """VersionUtilityのテスト"""

    def test_parse_version(self):
        """バージョン文字列の解析をテストする"""
        # 正常なバージョン
        major, minor, patch = VersionUtility.parse_version("1.2.3")
        assert major == 1
        assert minor == 2
        assert patch == 3

        # 不正なバージョン
        with pytest.raises(ValueError):
            VersionUtility.parse_version("1.2")

        with pytest.raises(ValueError):
            VersionUtility.parse_version("1.2.3.4")

        with pytest.raises(ValueError):
            VersionUtility.parse_version("a.b.c")

    def test_format_version(self):
        """バージョン文字列のフォーマットをテストする"""
        version = VersionUtility.format_version(1, 2, 3)
        assert version == "1.2.3"

    def test_increment_version(self):
        """バージョンのインクリメントをテストする"""
        # メジャーバージョンのインクリメント
        version = VersionUtility.increment_version("1.2.3", "major")
        assert version == "2.0.0"

        # マイナーバージョンのインクリメント
        version = VersionUtility.increment_version("1.2.3", "minor")
        assert version == "1.3.0"

        # パッチバージョンのインクリメント
        version = VersionUtility.increment_version("1.2.3", "patch")
        assert version == "1.2.4"

        # 不正なバージョンタイプ
        with pytest.raises(ValueError):
            VersionUtility.increment_version("1.2.3", "invalid")

    def test_compare_versions(self):
        """バージョンの比較をテストする"""
        # 等しいバージョン
        assert VersionUtility.compare_versions("1.2.3", "1.2.3") == 0

        # 左が大きいケース
        assert VersionUtility.compare_versions("2.0.0", "1.9.9") == 1
        assert VersionUtility.compare_versions("1.3.0", "1.2.9") == 1
        assert VersionUtility.compare_versions("1.2.4", "1.2.3") == 1

        # 右が大きいケース
        assert VersionUtility.compare_versions("1.9.9", "2.0.0") == -1
        assert VersionUtility.compare_versions("1.2.9", "1.3.0") == -1
        assert VersionUtility.compare_versions("1.2.3", "1.2.4") == -1

    def test_is_valid_version(self):
        """バージョン文字列の妥当性チェックをテストする"""
        # 有効なバージョン
        assert VersionUtility.is_valid_version("1.2.3") is True
        assert VersionUtility.is_valid_version("0.0.0") is True
        assert VersionUtility.is_valid_version("999.999.999") is True

        # 無効なバージョン
        assert VersionUtility.is_valid_version("1.2") is False
        assert VersionUtility.is_valid_version("1.2.3.4") is False
        assert VersionUtility.is_valid_version("a.b.c") is False
        assert VersionUtility.is_valid_version("1.2.c") is False


class TestDocumentDiffUtility:
    """DocumentDiffUtilityのテスト"""

    def test_compute_section_diff_no_changes(self):
        """変更がない場合のセクション差分計算をテストする"""
        old_sections = [
            {"title": "セクション1", "content": "内容1"},
            {"title": "セクション2", "content": "内容2"}
        ]
        new_sections = [
            {"title": "セクション1", "content": "内容1"},
            {"title": "セクション2", "content": "内容2"}
        ]

        diff = DocumentDiffUtility.compute_section_diff(old_sections, new_sections)

        assert len(diff["added"]) == 0
        assert len(diff["removed"]) == 0
        assert len(diff["modified"]) == 0

    def test_compute_section_diff_with_added(self):
        """セクション追加時の差分計算をテストする"""
        old_sections = [
            {"title": "セクション1", "content": "内容1"}
        ]
        new_sections = [
            {"title": "セクション1", "content": "内容1"},
            {"title": "セクション2", "content": "内容2"}
        ]

        diff = DocumentDiffUtility.compute_section_diff(old_sections, new_sections)

        assert len(diff["added"]) == 1
        assert diff["added"][0]["title"] == "セクション2"
        assert len(diff["removed"]) == 0
        assert len(diff["modified"]) == 0

    def test_compute_section_diff_with_removed(self):
        """セクション削除時の差分計算をテストする"""
        old_sections = [
            {"title": "セクション1", "content": "内容1"},
            {"title": "セクション2", "content": "内容2"}
        ]
        new_sections = [
            {"title": "セクション1", "content": "内容1"}
        ]

        diff = DocumentDiffUtility.compute_section_diff(old_sections, new_sections)

        assert len(diff["added"]) == 0
        assert len(diff["removed"]) == 1
        assert diff["removed"][0]["title"] == "セクション2"
        assert len(diff["modified"]) == 0

    def test_compute_section_diff_with_modified(self):
        """セクション変更時の差分計算をテストする"""
        old_sections = [
            {"title": "セクション1", "content": "内容1"},
            {"title": "セクション2", "content": "古い内容"}
        ]
        new_sections = [
            {"title": "セクション1", "content": "内容1"},
            {"title": "セクション2", "content": "新しい内容"}
        ]

        diff = DocumentDiffUtility.compute_section_diff(old_sections, new_sections)

        assert len(diff["added"]) == 0
        assert len(diff["removed"]) == 0
        assert len(diff["modified"]) == 1
        assert diff["modified"][0]["title"] == "セクション2"
        assert diff["modified"][0]["old_content"] == "古い内容"
        assert diff["modified"][0]["new_content"] == "新しい内容"

    def test_compute_section_diff_with_all_changes(self):
        """追加・削除・変更を含む差分計算をテストする"""
        old_sections = [
            {"title": "セクション1", "content": "内容1"},
            {"title": "セクション2", "content": "古い内容"},
            {"title": "削除されるセクション", "content": "削除対象"}
        ]
        new_sections = [
            {"title": "セクション1", "content": "内容1"},
            {"title": "セクション2", "content": "新しい内容"},
            {"title": "新しいセクション", "content": "追加された内容"}
        ]

        diff = DocumentDiffUtility.compute_section_diff(old_sections, new_sections)

        assert len(diff["added"]) == 1
        assert diff["added"][0]["title"] == "新しいセクション"

        assert len(diff["removed"]) == 1
        assert diff["removed"][0]["title"] == "削除されるセクション"

        assert len(diff["modified"]) == 1
        assert diff["modified"][0]["title"] == "セクション2"

    def test_create_revision_diff(self):
        """リビジョン差分オブジェクトの生成をテストする"""
        old_content = {
            "title": "ドキュメントタイトル",
            "sections": [
                {"title": "セクション1", "content": "内容1"},
                {"title": "セクション2", "content": "古い内容"},
                {"title": "削除されるセクション", "content": "削除対象"}
            ]
        }
        new_content = {
            "title": "ドキュメントタイトル",
            "sections": [
                {"title": "セクション1", "content": "内容1"},
                {"title": "セクション2", "content": "新しい内容"},
                {"title": "新しいセクション", "content": "追加された内容"}
            ]
        }

        diff = DocumentDiffUtility.create_revision_diff(old_content, new_content)

        # Pydanticモデルの検証
        assert len(diff.sections_added) == 1
        assert diff.sections_added[0].title == "新しいセクション"

        assert len(diff.sections_removed) == 1
        assert diff.sections_removed[0].title == "削除されるセクション"

        assert len(diff.sections_modified) == 1
        assert diff.sections_modified[0]["title"] == "セクション2"

        # バージョン情報は呼び出し側で設定されるため空
        assert diff.from_version == ""
        assert diff.to_version == ""


class TestDocumentService:
    """DocumentServiceのテスト"""

    @pytest.fixture
    def mock_storage(self):
        """ストレージサービスのモックを作成する"""
        with patch('src.services.document.get_storage_service') as mock_get_storage:
            # 通常のMagicMockを作成（同期メソッド用）
            mock_storage = MagicMock()
            mock_get_storage.return_value = mock_storage

            # 非同期メソッドをAsyncMockで設定
            mock_storage.save_content = AsyncMock(return_value="documents/test-id/1.0.0.json")
            mock_storage.load_content = AsyncMock(return_value={"title": "テスト", "sections": []})
            mock_storage.delete_content = AsyncMock(return_value=True)
            mock_storage.list_contents = AsyncMock(return_value=["documents/test-id/1.0.0.json", "documents/test-id/1.1.0.json"])

            # 同期メソッドの戻り値を通常のMagicMockで設定
            mock_storage.get_storage_key.return_value = "documents/test-id/1.0.0.json"

            yield mock_storage

    @pytest.fixture
    def document_service(self, mock_storage):
        """テスト用のDocumentServiceインスタンスを作成する"""
        return DocumentService()

    @pytest.mark.asyncio
    async def test_save_content(self, document_service, mock_storage):
        """コンテンツの保存をテストする"""
        # テスト実行
        content = {"title": "テスト", "sections": []}
        result = await document_service.save_content(content, "test-id", "1.0.0")

        # 検証
        mock_storage.save_content.assert_called_once_with(content, "test-id", "1.0.0")
        assert result == "documents/test-id/1.0.0.json"

    @pytest.mark.asyncio
    async def test_load_content(self, document_service, mock_storage):
        """コンテンツの読み込みをテストする"""
        # テスト実行
        storage_key = "documents/test-id/1.0.0.json"
        result = await document_service.load_content(storage_key)

        # 検証
        mock_storage.load_content.assert_called_once_with(storage_key)
        assert result == {"title": "テスト", "sections": []}

    @pytest.mark.asyncio
    async def test_delete_content(self, document_service, mock_storage):
        """コンテンツの削除をテストする"""
        # テスト実行
        storage_key = "documents/test-id/1.0.0.json"
        result = await document_service.delete_content(storage_key)

        # 検証
        mock_storage.delete_content.assert_called_once_with(storage_key)
        assert result is True

    @pytest.mark.asyncio
    async def test_list_document_versions(self, document_service, mock_storage):
        """ドキュメントバージョンのリスト取得をテストする"""
        # テスト実行
        result = await document_service.list_document_versions("test-id")

        # 検証
        mock_storage.list_contents.assert_called_once_with("documents/test-id")
        assert result == ["documents/test-id/1.0.0.json", "documents/test-id/1.1.0.json"]

    def test_get_storage_key(self, document_service, mock_storage):
        """ストレージキーの取得をテストする"""
        # テスト実行
        result = document_service.get_storage_key("test-id", "1.0.0")

        # 検証
        mock_storage.get_storage_key.assert_called_once_with("test-id", "1.0.0")
        assert result == "documents/test-id/1.0.0.json"
