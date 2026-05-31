from __future__ import annotations

from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape


class PlayerLayoutRenderer:
    REFRESH_LOGO = (
        "M914.17946 324.34283C854.308387 324.325508 750.895846 324.317788 "
        "750.895846 324.317788 732.045471 324.317788 716.764213 339.599801 "
        "716.764213 358.451121 716.764213 377.30244 732.045471 392.584453 "
        "750.895846 392.584453L955.787864 392.584453C993.448095 392.584453 "
        "1024 362.040424 1024 324.368908L1024 119.466667C1024 100.615347 "
        "1008.718742 85.333333 989.868367 85.333333 971.017993 85.333333 "
        "955.736735 100.615347 955.736735 119.466667L955.736735 256.497996C"
        "933.314348 217.628194 905.827487 181.795372 873.995034 149.961328 "
        "778.623011 54.584531 649.577119 0 511.974435 0 229.218763 0 0 "
        "229.230209 0 512 0 794.769791 229.218763 1024 511.974435 1024 "
        "794.730125 1024 1023.948888 794.769791 1023.948888 512 1023.948888 "
        "493.148681 1008.66763 477.866667 989.817256 477.866667 970.966881 "
        "477.866667 955.685623 493.148681 955.685623 512 955.685623 "
        "757.067153 757.029358 955.733333 511.974435 955.733333 266.91953 "
        "955.733333 68.263265 757.067153 68.263265 512 68.263265 266.932847 "
        "266.91953 68.266667 511.974435 68.266667 631.286484 68.266667 "
        "743.028524 115.531923 825.725634 198.233152 862.329644 234.839003 "
        "892.298522 277.528256 914.17946 324.34283L914.17946 324.34283Z"
    )

    def render(self, players: Iterable[str], empty_text: str = "暂无玩家") -> str:
        player_list = [player.strip() for player in players if player and player.strip()]
        body = self._render_empty_row(empty_text) if not player_list else self._render_player_rows(player_list)
        return "\n".join(
            [
                '<local:MyCard Margin="0,0,0,0" CanSwap="False" IsSwapped="True">',
                '    <StackPanel Margin="10">',
                '        <Grid Margin="0,0,0,12">',
                '            <Grid.ColumnDefinitions>',
                '                <ColumnDefinition Width="*" />',
                '                <ColumnDefinition Width="Auto" />',
                '            </Grid.ColumnDefinitions>',
                "",
                '            <TextBlock VerticalAlignment="Center"',
                '                       FontSize="16"',
                '                       FontWeight="Bold"',
                '                       Text="在线玩家" />',
                "",
                '            <local:MyIconTextButton Grid.Column="1"',
                '                                    Width="Auto"',
                '                                    Height="Auto"',
                '                                    HorizontalAlignment="Right"',
                '                                    ColorType="Highlight"',
                '                                    Text=""',
                '                                    EventType="刷新主页"',
                '                                    LogoScale="1"',
                f'                                    Logo="{self.REFRESH_LOGO}" />',
                "        </Grid>",
                body,
                "    </StackPanel>",
                "</local:MyCard>",
            ]
        )

    def write(self, players: Iterable[str], path: str | Path = "Custom.xaml", empty_text: str = "暂无玩家") -> str:
        xaml = self.render(players, empty_text=empty_text)
        Path(path).write_text(xaml, encoding="utf-8")
        return xaml

    def _render_empty_row(self, text: str) -> str:
        cards = [self._render_empty_card(column, margin, text) for column, margin in self._column_margins(1)]
        return self._wrap_row(cards)

    def _render_player_rows(self, players: list[str]) -> str:
        rows = []
        for start in range(0, len(players), 3):
            chunk = players[start : start + 3]
            cards = [
                self._render_player_card(name, column, margin)
                for (column, margin), name in zip(self._column_margins(len(chunk)), chunk)
            ]
            rows.append(self._wrap_row(cards))
        return "\n".join(rows)

    def _wrap_row(self, cards: list[str]) -> str:
        indented_cards = "\n".join(self._indent_lines(card, 3) for card in cards)
        return "\n".join(
            [
                '        <Grid Margin="0,0,0,12">',
                '            <Grid.ColumnDefinitions>',
                '                <ColumnDefinition Width="*" />',
                '                <ColumnDefinition Width="*" />',
                '                <ColumnDefinition Width="*" />',
                '            </Grid.ColumnDefinitions>',
                indented_cards,
                "        </Grid>",
            ]
        )

    def _render_player_card(self, name: str, column: int, margin: str) -> str:
        safe_name = escape(name)
        return "\n".join(
            [
                f'<Border Grid.Column="{column}"',
                f'        Margin="{margin}"',
                '        Padding="12,10"',
                '        Background="#F4F7FB"',
                '        BorderBrush="#D8E0EA"',
                '        BorderThickness="1"',
                '        CornerRadius="10">',
                "    <StackPanel>",
                '        <TextBlock FontSize="14"',
                '                   FontWeight="Bold"',
                '                   Foreground="#2F3E4E"',
                f'                   Text="{safe_name}" />',
                "    </StackPanel>",
                "</Border>",
            ]
        )

    def _render_empty_card(self, column: int, margin: str, text: str) -> str:
        safe_text = escape(text)
        return "\n".join(
            [
                f'<Border Grid.Column="{column}"',
                f'        Margin="{margin}"',
                '        Padding="12,10"',
                '        Background="#F4F7FB"',
                '        BorderBrush="#D8E0EA"',
                '        BorderThickness="1"',
                '        CornerRadius="10">',
                "    <StackPanel>",
                '        <TextBlock FontSize="14"',
                '                   FontWeight="Bold"',
                '                   Foreground="#6B7A8C"',
                f'                   Text="{safe_text}" />',
                "    </StackPanel>",
                "</Border>",
            ]
        )

    def _column_margins(self, count: int) -> list[tuple[int, str]]:
        margins = ["0,0,6,0", "3,0", "6,0,0,0"]
        return [(index, margins[index]) for index in range(count)]

    @staticmethod
    def _indent_lines(text: str, level: int) -> str:
        prefix = "    " * level
        return "\n".join(f"{prefix}{line}" for line in text.splitlines())
