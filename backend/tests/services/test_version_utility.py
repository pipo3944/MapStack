import pytest
from src.services.document import VersionUtility

class TestVersionUtility:
    """VersionUtilityクラスのテスト"""

    def test_parse_version_valid(self):
        """有効なバージョン文字列のパースをテスト"""
        result = VersionUtility.parse_version("1.2.3")
        assert result == (1, 2, 3)

        result = VersionUtility.parse_version("0.0.1")
        assert result == (0, 0, 1)

        result = VersionUtility.parse_version("10.20.30")
        assert result == (10, 20, 30)

    def test_parse_version_invalid(self):
        """無効なバージョン文字列のパースをテスト"""
        # フォーマットが不正な場合
        with pytest.raises(ValueError, match="Invalid version format"):
            VersionUtility.parse_version("1.2")

        with pytest.raises(ValueError, match="Invalid version format"):
            VersionUtility.parse_version("1.2.3.4")

        # 数値でない部分を含む場合
        with pytest.raises(ValueError, match="Version parts must be integers"):
            VersionUtility.parse_version("1.2.a")

        with pytest.raises(ValueError, match="Version parts must be integers"):
            VersionUtility.parse_version("a.b.c")

    def test_format_version(self):
        """バージョン番号のフォーマットをテスト"""
        result = VersionUtility.format_version(1, 2, 3)
        assert result == "1.2.3"

        result = VersionUtility.format_version(0, 0, 1)
        assert result == "0.0.1"

        result = VersionUtility.format_version(10, 20, 30)
        assert result == "10.20.30"

    def test_increment_version_major(self):
        """メジャーバージョンのインクリメントをテスト"""
        result = VersionUtility.increment_version("1.2.3", "major")
        assert result == "2.0.0"

        result = VersionUtility.increment_version("0.9.9", "major")
        assert result == "1.0.0"

    def test_increment_version_minor(self):
        """マイナーバージョンのインクリメントをテスト"""
        result = VersionUtility.increment_version("1.2.3", "minor")
        assert result == "1.3.0"

        result = VersionUtility.increment_version("1.9.9", "minor")
        assert result == "1.10.0"

    def test_increment_version_patch(self):
        """パッチバージョンのインクリメントをテスト"""
        result = VersionUtility.increment_version("1.2.3", "patch")
        assert result == "1.2.4"

        result = VersionUtility.increment_version("1.2.9", "patch")
        assert result == "1.2.10"

    def test_increment_version_invalid_type(self):
        """無効なバージョンタイプでのインクリメントをテスト"""
        with pytest.raises(ValueError, match="Invalid version type"):
            VersionUtility.increment_version("1.2.3", "invalid")

    def test_compare_versions_equal(self):
        """同じバージョンの比較をテスト"""
        result = VersionUtility.compare_versions("1.2.3", "1.2.3")
        assert result == 0

    def test_compare_versions_greater(self):
        """より大きいバージョンの比較をテスト"""
        # メジャーバージョンが大きい
        result = VersionUtility.compare_versions("2.0.0", "1.9.9")
        assert result == 1

        # マイナーバージョンが大きい
        result = VersionUtility.compare_versions("1.3.0", "1.2.9")
        assert result == 1

        # パッチバージョンが大きい
        result = VersionUtility.compare_versions("1.2.4", "1.2.3")
        assert result == 1

    def test_compare_versions_less(self):
        """より小さいバージョンの比較をテスト"""
        # メジャーバージョンが小さい
        result = VersionUtility.compare_versions("1.9.9", "2.0.0")
        assert result == -1

        # マイナーバージョンが小さい
        result = VersionUtility.compare_versions("1.2.9", "1.3.0")
        assert result == -1

        # パッチバージョンが小さい
        result = VersionUtility.compare_versions("1.2.3", "1.2.4")
        assert result == -1

    def test_is_valid_version(self):
        """バージョン文字列の有効性チェックをテスト"""
        assert VersionUtility.is_valid_version("1.2.3") is True
        assert VersionUtility.is_valid_version("0.0.1") is True
        assert VersionUtility.is_valid_version("10.20.30") is True

        assert VersionUtility.is_valid_version("1.2") is False
        assert VersionUtility.is_valid_version("1.2.3.4") is False
        assert VersionUtility.is_valid_version("1.2.a") is False
        assert VersionUtility.is_valid_version("a.b.c") is False

    def test_determine_version_type_title_change(self):
        """タイトル変更時のバージョンタイプ決定をテスト"""
        old_content = {
            "title": "古いタイトル",
            "sections": [{"title": "セクション1", "content": "内容1"}]
        }
        new_content = {
            "title": "新しいタイトル",  # タイトル変更
            "sections": [{"title": "セクション1", "content": "内容1"}]
        }

        result = VersionUtility.determine_version_type(old_content, new_content)
        assert result == "minor"

    def test_determine_version_type_section_add(self):
        """セクション追加時のバージョンタイプ決定をテスト"""
        old_content = {
            "title": "タイトル",
            "sections": [{"title": "セクション1", "content": "内容1"}]
        }
        new_content = {
            "title": "タイトル",
            "sections": [
                {"title": "セクション1", "content": "内容1"},
                {"title": "セクション2", "content": "内容2"}  # セクション追加
            ]
        }

        result = VersionUtility.determine_version_type(old_content, new_content)
        assert result == "minor"

    def test_determine_version_type_section_remove(self):
        """セクション削除時のバージョンタイプ決定をテスト"""
        old_content = {
            "title": "タイトル",
            "sections": [
                {"title": "セクション1", "content": "内容1"},
                {"title": "セクション2", "content": "内容2"}
            ]
        }
        new_content = {
            "title": "タイトル",
            "sections": [{"title": "セクション1", "content": "内容1"}]  # セクション削除
        }

        result = VersionUtility.determine_version_type(old_content, new_content)
        assert result == "minor"

    def test_determine_version_type_section_title_change(self):
        """セクションタイトル変更時のバージョンタイプ決定をテスト"""
        old_content = {
            "title": "タイトル",
            "sections": [{"title": "古いセクションタイトル", "content": "内容1"}]
        }
        new_content = {
            "title": "タイトル",
            "sections": [{"title": "新しいセクションタイトル", "content": "内容1"}]  # セクションタイトル変更
        }

        result = VersionUtility.determine_version_type(old_content, new_content)
        assert result == "minor"

    def test_determine_version_type_significant_content_change(self):
        """内容の大きな変更時のバージョンタイプ決定をテスト"""
        old_content = {
            "title": "タイトル",
            "sections": [{"title": "セクション1", "content": "短い内容"}]
        }
        new_content = {
            "title": "タイトル",
            "sections": [{"title": "セクション1", "content": "非常に長い内容"*20}]  # 内容の大きな変更
        }

        result = VersionUtility.determine_version_type(old_content, new_content)
        assert result == "minor"

    def test_determine_version_type_minor_content_change(self):
        """内容の小さな変更時のバージョンタイプ決定をテスト"""
        old_content = {
            "title": "タイトル",
            "sections": [{"title": "セクション1", "content": "元の内容です"}]
        }
        new_content = {
            "title": "タイトル",
            "sections": [{"title": "セクション1", "content": "少し修正した内容です"}]  # 内容の小さな変更
        }

        result = VersionUtility.determine_version_type(old_content, new_content)
        assert result == "patch"

    def test_determine_version_type_no_change(self):
        """変更がない場合のバージョンタイプ決定をテスト"""
        content = {
            "title": "タイトル",
            "sections": [{"title": "セクション1", "content": "内容1"}]
        }

        result = VersionUtility.determine_version_type(content, content)
        assert result == "patch"  # 変更がなくてもpatchとして扱う
