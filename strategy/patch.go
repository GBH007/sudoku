package strategy

type Patch struct {
	row         int
	column      int
	number      int
	Efficieny   int
	Alternative *Patch
}

func NewPatch(row, col, num int) *Patch {
	return &Patch{row: row, column: col, number: num}
}

func (p *Patch) Row() int    { return p.row }
func (p *Patch) Column() int { return p.column }
func (p *Patch) Number() int { return p.number }
