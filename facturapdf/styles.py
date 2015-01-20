from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet


class DefaultStyling:
    CELL_TITLES_BACKGROUND_COLOR = HexColor(0x0096FF)

    styles = getSampleStyleSheet()

    def __init__(self):
        self.table = ([
            ('GRID', (0, 0), (-1, -1), 0.6, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), self.CELL_TITLES_BACKGROUND_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ])

        self.invoice_text = self.styles.get('Normal')

        self.table_rows_with_subtotal = [
            ('GRID', (0, 0), (-1, 0), 0.6, colors.black),
            ('BOX', (0, 1), (-1, -2), 0.6, colors.black),

            # Titles
            ('BACKGROUND', (0, 0), (-1, 0), self.CELL_TITLES_BACKGROUND_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

            # Align prices to the right
            ('ALIGN', (1, 1), (-1, -2), 'RIGHT'),
            ('ALIGN', (-1, -1), (-1, -1), 'RIGHT'),

            # Subtotal
            ('TEXTCOLOR', (2, -1), (-2, -1), colors.white),
            ('BACKGROUND', (2, -1), (-2, -1), self.CELL_TITLES_BACKGROUND_COLOR),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('GRID', (2, -1), (-1, -1), 0.6, colors.black)
        ]

        self.table_rows_without_subtotal = [
            ('GRID', (0, 0), (-1, 0), 0.6, colors.black),
            ('BOX', (0, 1), (-1, -1), 0.6, colors.black),

            # Titles
            ('BACKGROUND', (0, 0), (-1, 0), self.CELL_TITLES_BACKGROUND_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

            # Align prices to the right
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('ALIGN', (-1, -1), (-1, -1), 'RIGHT'),
        ]