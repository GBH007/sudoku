package strategy

import "sudoku/data"

/*
maximum count of allocated numbers
максимальное количество размещенных чисел
стратегия в которой лучшим решением является цифра которой больше всего на поле
*/
type MaxCoAN struct {
	c *data.Controller
}

func NewMaxCoAN(c *data.Controller) *MaxCoAN {
	mpc := new(MaxCoAN)
	mpc.Init(c)
	return mpc
}
func (mpc *MaxCoAN) Init(c *data.Controller) {
	mpc.c = c
}
func (mpc *MaxCoAN) Name() string { return "MaxCoAN" }
func (mpc *MaxCoAN) GetResult() []*data.Patch {
	res := make([]*data.Patch, 0)
	num := mpc.c.GetMinCountOfRemainingNumber()
	for _, cell := range mpc.c.GetPossibleCellForNumber(num) {
		res = append(res, data.NewPatch(cell/9, cell%9, num))
	}
	return res
}
