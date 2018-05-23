package strategy

import "sudoku/data"

/*
maximum count of allocated numbers
максимальное количество размещенных чисел
стратегия в которой лучшим решением является цифра которой больше всего на поле
*/
type MaxCoAN struct {
	sdc *data.SudokuDataController
}

func NewMaxCoAN(sdc *data.SudokuDataController) *MaxCoAN {
	mpc := new(MaxCoAN)
	mpc.Init(sdc)
	return mpc
}
func (mpc *MaxCoAN) Init(sdc *data.SudokuDataController) {
	mpc.sdc = sdc
}
func (mpc *MaxCoAN) Name() string { return "MaxCoAN" }
func (mpc *MaxCoAN) GetResult() []*Patch {
	res := make([]*Patch, 0)
	sdc := mpc.sdc
	num := getMaxElementIndexFromStart(sdc.GetCountNumber(), 1)
	//numCount := sdc.GetCountNumber()[num]
	positions := sdc.GetFreePositionForNumber(num)
	for pos, _ := range positions {
		patch := NewPatch(pos/9, pos%9, num)
		patch.Efficieny = sdc.CalculateEfficiency(patch) // * numCount
		patch.StrategyNames = []string{mpc.Name()}
		res = append(res, patch)
	}
	return res
}
