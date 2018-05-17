package strategy

import "sudoku/data"

type MaxPlaceCountStrategy struct {
	sdc *data.SudokuDataController
}

func NewMaxPlaceCountStrategy(sdc *data.SudokuDataController) *MaxPlaceCountStrategy {
	mpc := new(MaxPlaceCountStrategy)
	mpc.Init(sdc)
	return mpc
}
func (mpc *MaxPlaceCountStrategy) Init(sdc *data.SudokuDataController) {
	mpc.sdc = sdc
}
func (mpc *MaxPlaceCountStrategy) Name() string { return "MaxPlaceCountStrategy" }
func (mpc *MaxPlaceCountStrategy) GetResult() []*Patch {
	res := make([]*Patch, 0)
	sdc := mpc.sdc
	num := getMaxElementIndexFromStart(sdc.GetCountNumber(), 1)
	positions := sdc.GetFreePositionForNumber(num)
	for pos, _ := range positions {
		patch := NewPatch(pos/9, pos%9, num)
		patch.Efficieny = sdc.CalculateEfficiency(patch)
		patch.StrategyNames = []string{mpc.Name()}
		res = append(res, patch)
	}
	return res
}
