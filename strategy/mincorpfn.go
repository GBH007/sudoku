package strategy

import "sudoku/data"

/*
minimum count of remaining positions for number
минимальное количество оставшихся позиций для числа
стратегия в которой лучшей является цифра для которой меньше всего вариантов установки
*/
type MinCoRPFN struct {
	sdc *data.SudokuDataController
}

func NewMinCoRPFN(sdc *data.SudokuDataController) *MinCoRPFN {
	mpc := new(MinCoRPFN)
	mpc.Init(sdc)
	return mpc
}
func (mpc *MinCoRPFN) Init(sdc *data.SudokuDataController) {
	mpc.sdc = sdc
}
func (mpc *MinCoRPFN) Name() string { return "MinCoRPFN" }
func (mpc *MinCoRPFN) GetResult() []*Patch {
	res := make([]*Patch, 0)
	sdc := mpc.sdc
	num := 0
	numVal := 999
	for i := 1; i < 10; i++ {
		l := len(sdc.GetFreePositionForNumber(i))
		if l > 0 {
			if l < numVal {
				numVal = l
				num = i
			}
		}
	}
	positions := sdc.GetFreePositionForNumber(num)
	for pos, _ := range positions {
		patch := NewPatch(pos/9, pos%9, num)
		patch.Efficieny = sdc.CalculateEfficiency(patch)
		patch.StrategyNames = []string{mpc.Name()}
		res = append(res, patch)
	}
	return res
}
