package strategy

import "fmt"

type Patch struct {
	row       int
	column    int
	number    int
	Efficieny int
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
