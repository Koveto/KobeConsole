from constants import *

class Font:
    """
    Generic bitmap font loader for Pokémon-style fonts.
    Supports variable glyph width, height, scale, and spacing.
    """

    def __init__(self, filename, glyph_w, glyph_h, scale=4, spacing=None,row2=None):
        self.glyph_w = glyph_w
        self.glyph_h = glyph_h
        self.scale = scale
        self.row2 = row2

        # If spacing not provided, default to scaled width
        self.spacing = spacing if spacing is not None else glyph_w * scale

        font_path = os.path.join(TEXT_ROOT, "sprites", filename)

        # Load sheet (white = transparent)
        sheet = pygame.image.load(font_path).convert()
        sheet.set_colorkey((255,255,255))

        self.glyphs = {}
        self._slice_sheet(sheet)

    # ---------------------------------------------------------
    # Slice spritesheet into glyphs (scaled × self.scale)
    # ---------------------------------------------------------

    def _slice_sheet(self, sheet):
        """
        Cuts the sheet into glyphs and maps characters.
        """

        # Row 0: A-Z
        for i in range(26):
            rect = pygame.Rect(
                i * self.glyph_w,
                0,
                self.glyph_w,
                self.glyph_h
            )
            glyph = sheet.subsurface(rect)
            glyph = pygame.transform.scale(
                glyph,
                (self.glyph_w * self.scale, self.glyph_h * self.scale)
            )
            self.glyphs[chr(ord('A') + i)] = glyph

        # Row 1: a-z
        for i in range(26):
            rect = pygame.Rect(
                i * self.glyph_w,
                self.glyph_h,
                self.glyph_w,
                self.glyph_h
            )
            glyph = sheet.subsurface(rect)
            glyph = pygame.transform.scale(
                glyph,
                (self.glyph_w * self.scale, self.glyph_h * self.scale)
            )
            self.glyphs[chr(ord('a') + i)] = glyph

        # Row 2: digits + punctuation (26 glyphs)
        row2 = self.row2

        if row2 is None:
            row2 = "0123456789!?.-\"\"''/+"

        for i, ch in enumerate(row2):
            rect = pygame.Rect(
                i * self.glyph_w,
                self.glyph_h * 2,
                self.glyph_w,
                self.glyph_h
            )
            glyph = sheet.subsurface(rect)
            glyph = pygame.transform.scale(
                glyph,
                (self.glyph_w * self.scale, self.glyph_h * self.scale)
            )
            self.glyphs[ch] = glyph

        # Space is blank
        blank = pygame.Surface(
            (self.glyph_w * self.scale, self.glyph_h * self.scale),
            pygame.SRCALPHA
        )
        self.glyphs[" "] = blank

    # ---------------------------------------------------------
    # Draw text
    # ---------------------------------------------------------

    def draw_text(self, screen, text, x, y):
        """
        Draws text using the scaled bitmap font.
        """
        cx = x
        for ch in text:
            glyph = self.glyphs.get(ch)
            if glyph:
                screen.blit(glyph, (cx, y))
            cx += self.spacing