package strategy

import "sudoku/data"

/*
min set of numbers in the cell
минимальный набор чисел в ячейке
*/
type MinSoNitC struct {
	sdc *data.SudokuDataController
}

func NewMinSoNitC(sdc *data.SudokuDataController) *MinSoNitC {
	mpc := new(MinSoNitC)
	mpc.Init(sdc)
	return mpc
}
func (mpc *MinSoNitC) Init(sdc *data.SudokuDataController) {
	mpc.sdc = sdc
}
func (mpc *MinSoNitC) Name() string { return "MinSoNitC" }
func (mpc *MinSoNitC) GetResult() []*Patch {
	res := make([]*Patch, 0)
	sdc := mpc.sdc
	ind := 0
	numVal := 999
	cc := sdc.GetCountCell()
	for i, l := range cc {
		if l > 0 {
			if l < numVal {
				numVal = l
				ind = i
			}
		}
	}
	for num := 1; num < 10; num++ {
		if !sdc.IsPossibleInstall(ind/9, ind%9, num) {
			continue
		}
		patch := NewPatch(ind/9, ind%9, num)
		patch.Efficieny = sdc.CalculateEfficiency(patch)
		patch.StrategyNames = []string{mpc.Name()}
		res = append(res, patch)
	}
	return res
}
