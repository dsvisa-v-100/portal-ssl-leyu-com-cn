from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    """关键词笔记的数据类"""
    keyword: str
    note: str
    source_url: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: Optional[str] = None
    priority: int = 0

    def update_note(self, new_note: str) -> None:
        self.note = new_note
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "note": self.note,
            "source_url": self.source_url,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "priority": self.priority,
        }


@dataclass
class KeywordCollection:
    """管理多个关键词笔记的集合"""
    collection_name: str
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> Optional[KeywordNote]:
        for note in self.notes:
            if note.keyword == keyword:
                return note
        return None

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [note for note in self.notes if tag in note.tags]

    def sort_by_priority(self, reverse: bool = False) -> List[KeywordNote]:
        return sorted(self.notes, key=lambda note: note.priority, reverse=reverse)


def format_note_single(note: KeywordNote) -> str:
    """格式化单个笔记为可读字符串"""
    parts = [
        f"关键词: {note.keyword}",
        f"笔记: {note.note}",
        f"来源: {note.source_url or '无'}",
        f"标签: {', '.join(note.tags) if note.tags else '无'}",
        f"创建时间: {note.created_at}",
        f"更新时间: {note.updated_at or '未更新'}",
        f"优先级: {note.priority}",
    ]
    return "\n".join(parts)


def format_note_table(notes: List[KeywordNote]) -> str:
    """将笔记列表格式化为表格形式"""
    if not notes:
        return "无记录"
    header = f"{'关键词':<12} {'笔记':<20} {'来源':<20} {'标签':<16} {'优先级':<6}"
    separator = "-" * 80
    lines = [header, separator]
    for note in notes:
        tags = ", ".join(note.tags) if note.tags else "-"
        source = note.source_url if note.source_url else "-"
        lines.append(f"{note.keyword:<12} {note.note[:18]:<20} {source[:18]:<20} {tags:<16} {note.priority:<6}")
    return "\n".join(lines)


def build_demo_data() -> KeywordCollection:
    """构建示例数据，展示功能"""
    collection = KeywordCollection(collection_name="示例笔记")

    note1 = KeywordNote(
        keyword="乐鱼体育",
        note="关注乐鱼体育的最新动态与赛事信息。",
        source_url="https://portal-ssl-leyu.com.cn",
        tags=["体育", "乐鱼"],
        priority=3,
    )
    note2 = KeywordNote(
        keyword="Python",
        note="Python 是一种解释型高级编程语言。",
        source_url="https://python.org",
        tags=["编程", "语言"],
        priority=1,
    )
    note3 = KeywordNote(
        keyword="乐鱼体育",
        note="关于乐鱼体育的赛事报道与分析。",
        source_url="https://portal-ssl-leyu.com.cn/news",
        tags=["体育", "乐鱼", "赛事"],
        priority=2,
    )
    note4 = KeywordNote(
        keyword="体育新闻",
        note="汇总体育新闻与热门赛事。",
        tags=["体育", "新闻"],
        priority=0,
    )
    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)
    collection.add_note(note4)
    return collection


if __name__ == "__main__":
    collection = build_demo_data()
    print(f"合集: {collection.collection_name}\n")
    print("所有笔记表格形式:")
    print(format_note_table(collection.notes))
    print("\n按关键词查找 '乐鱼体育':")
    found = collection.find_by_keyword("乐鱼体育")
    if found:
        print(format_note_single(found))
    else:
        print("未找到")
    print("\n按标签 '体育' 筛选:")
    sports_notes = collection.find_by_tag("体育")
    print(format_note_table(sports_notes))
    print("\n按优先级排序（降序）:")
    sorted_notes = collection.sort_by_priority(reverse=True)
    print(format_note_table(sorted_notes))