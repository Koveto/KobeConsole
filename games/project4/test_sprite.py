"""PlayerGfxHandler:
        lda InjuryTimer             ;if player's injured invincibility timer
        beq CntPl                   ;not set, skip checkpoint and continue code
        lda FrameCounter
        lsr                         ;otherwise check frame counter and branch
        bcs ExPGH                   ;to leave on every other frame (when d0 is set)​‌
PlayerInter:   jsr DrawPlayer_Intermediate  ;put player in appropriate place for
               lda #$01                     ;lives display, then output lives display to buffer​‌
DrawPlayer_Intermediate:
          ldx #$05                       ;store data into zero page memory​‌
DrawPlayerLoop:
        lda PlayerGraphicsTable,x    ;load player's left side
        sta $00
        lda PlayerGraphicsTable+1,x  ;now load right side
        jsr DrawOneSpriteRow
        dec $07                      ;decrement rows of sprites to draw
        bne DrawPlayerLoop           ;do this until all rows are drawn
        rts​‌
PlayerInter:   jsr DrawPlayer_Intermediate  ;put player in appropriate place for
               lda #$01                     ;lives display, then output lives display to buffer​‌

RenderSprite doesn't exist by that name​‌

PlayerGraphicsTable:
;big player table
      .db $00, $01, $02, $03, $04, $05, $06, $07 ;walking frame 1
      .db $08, $09, $0a, $0b, $0c, $0d, $0e, $0f ;        frame 2
      .db $10, $11, $12, $13, $14, $15, $16, $17 ;        frame 3
      .db $18, $19, $1a, $1b, $1c, $1d, $1e, $1f ;skidding
      .db $20, $21, $22, $23, $24, $25, $26, $27 ;jumping
      .db $08, $09, $28, $29, $2a, $2b, $2c, $2d ;swimming frame 1
      .db $08, $09, $0a, $0b, $0c, $30, $2c, $2d ;         frame 2
      .db $08, $09, $0a, $0b, $2e, $2f, $2c, $2d ;         frame 3
      .db $08, $09, $28, $29, $2a, $2b, $5c, $5d ;climbing frame 1
      .db $08, $09, $0a, $0b, $0c, $0d, $5e, $5f ;         frame 2
      .db $fc, $fc, $08, $09, $58, $59, $5a, $5a ;crouching
      .db $08, $09, $28, $29, $2a, $2b, $0e, $0f ;fireball throwing

;small player table
      .db $fc, $fc, $fc, $fc, $32, $33, $34, $35 ;walking frame 1
      .db $fc, $fc, $fc, $fc, $36, $37, $38, $39 ;        frame 2
      .db $fc, $fc, $fc, $fc, $3a, $37, $3b, $3c ;        frame 3
      .db $fc, $fc, $fc, $fc, $3d, $3e, $3f, $40 ;skidding
      .db $fc, $fc, $fc, $fc, $32, $41, $42, $43 ;jumping
      .db $fc, $fc, $fc, $fc, $32, $33, $44, $45 ;swimming frame 1
      .db $fc, $fc, $fc, $fc, $32, $33, $44, $47 ;         frame 2
      .db $fc, $fc, $fc, $fc, $32, $33, $48, $49 ;         frame 3
      .db $fc, $fc, $fc, $fc, $32, $33, $90, $91 ;climbing frame 1
      .db $fc, $fc, $fc, $fc, $3a, $37, $92, $93 ;         frame 2
      .db $fc, $fc, $fc, $fc, $9e, $9e, $9f, $9f ;killed

;used by both player sizes
      .db $fc, $fc, $fc, $fc, $3a, $37, $4f, $4f ;small player standing
      .db $fc, $fc, $00, $01, $4c, $4d, $4e, $4e ;intermediate grow frame
      .db $00, $01, $4c, $4d, $4a, $4a, $4b, $4b ;big player standing​‌

"""