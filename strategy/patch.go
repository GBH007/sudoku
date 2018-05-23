package strategy

import (
	"fmt"
	"strings"
)

type Patch struct {
	row           int
	column        int
	number        int
	Efficieny     int
	StrategyNames []string
}

func NewPatch(row, col, num int) *Patch {
	return &Patch{row: row, column: col, number: num}
}

func (p *Patch) Row() int    { return p.row }
func (p *Patch) Column() int { return p.column }
func (p *Patch) Number() int { return p.number }
func (p *Patch) String() string {
	return fmt.Sprintf("%d %d : %d -> %d", p.row, p.column, p.number, p.Efficieny)
}
func (p *Patch) ToLog() string {
	return fmt.Sprintf("%d %d : %d -> %d |=| %s", p.row, p.column, p.number, p.Efficieny, strings.Join(p.StrategyNames, ", "))
}
func (p *Patch) GetUUID() int {
	return p.column + p.row*9 + p.number*100
}

type PatchList []*Patch

//по умолчанию сортирует в порядке неувеличения эффективности
func (pl PatchList) Len() int           { return len(pl) }
func (pl PatchList) Less(i, j int) bool { return pl[i].Efficieny < pl[j].Efficieny }
func (pl PatchList) Swap(i, j int)      { pl[i], pl[j] = pl[j], pl[i] }
