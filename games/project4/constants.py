#CONSTANTS

#sound effects constants
Sfx_SmallJump         = 0b10000000
Sfx_Flagpole          = 0b01000000
Sfx_Fireball          = 0b00100000
Sfx_PipeDown_Injury   = 0b00010000
Sfx_EnemySmack        = 0b00001000
Sfx_EnemyStomp        = 0b00000100
Sfx_Bump              = 0b00000010
Sfx_BigJump           = 0b00000001

Sfx_BowserFall        = 0b10000000
Sfx_ExtraLife         = 0b01000000
Sfx_PowerUpGrab       = 0b00100000
Sfx_TimerTick         = 0b00010000
Sfx_Blast             = 0b00001000
Sfx_GrowVine          = 0b00000100
Sfx_GrowPowerUp       = 0b00000010
Sfx_CoinGrab          = 0b00000001

Sfx_BowserFlame       = 0b00000010
Sfx_BrickShatter      = 0b00000001

#music constants
Silence               = 0b10000000

StarPowerMusic        = 0b01000000
PipeIntroMusic        = 0b00100000
CloudMusic            = 0b00010000
CastleMusic           = 0b00001000
UndergroundMusic      = 0b00000100
WaterMusic            = 0b00000010
GroundMusic           = 0b00000001

TimeRunningOutMusic   = 0b01000000
EndOfLevelMusic       = 0b00100000
AltGameOverMusic      = 0b00010000
EndOfCastleMusic      = 0b00001000
VictoryMusic          = 0b00000100
GameOverMusic         = 0b00000010
DeathMusic            = 0b00000001

#enemy object constants 
GreenKoopa            = 0x00
BuzzyBeetle           = 0x02
RedKoopa              = 0x03
HammerBro             = 0x05
Goomba                = 0x06
Bloober               = 0x07
BulletBill_FrenzyVar  = 0x08
GreyCheepCheep        = 0x0a
RedCheepCheep         = 0x0b
Podoboo               = 0x0c
PiranhaPlant          = 0x0d
GreenParatroopaJump   = 0x0e
RedParatroopa         = 0x0f
GreenParatroopaFly    = 0x10
Lakitu                = 0x11
Spiny                 = 0x12
FlyCheepCheepFrenzy   = 0x14
FlyingCheepCheep      = 0x14
BowserFlame           = 0x15
Fireworks             = 0x16
BBill_CCheep_Frenzy   = 0x17
Stop_Frenzy           = 0x18
Bowser                = 0x2d
PowerUpObject         = 0x2e
VineObject            = 0x2f
FlagpoleFlagObject    = 0x30
StarFlagObject        = 0x31
JumpspringObject      = 0x32
BulletBill_CannonVar  = 0x33
RetainerObject        = 0x35
TallEnemy             = 0x09

#other constants
World1 = 0
World2 = 1
World3 = 2
World4 = 3
World5 = 4
World6 = 5
World7 = 6
World8 = 7
Level1 = 0
Level2 = 1
Level3 = 2
Level4 = 3

WarmBootOffset        = 0xd6
ColdBootOffset        = 0xfe
TitleScreenDataOffset = 0x1ec0
SoundMemory           = 0x07b0
#SwimTileRepOffset     = PlayerGraphicsTable + 0x9e
#MusicHeaderOffsetData = MusicHeaderData - 1
#MHD                   = MusicHeaderData

A_Button              = 0b10000000
B_Button              = 0b01000000
Select_Button         = 0b00100000
Start_Button          = 0b00010000
Up_Dir                = 0b00001000
Down_Dir              = 0b00000100
Left_Dir              = 0b00000010
Right_Dir             = 0b00000001

TitleScreenModeValue  = 0
GameModeValue         = 1
VictoryModeValue      = 2
GameOverModeValue     = 3