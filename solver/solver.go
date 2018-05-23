package solver

import (
	"sort"
	"sudoku/data"
	"sudoku/strategy"
)

type Solver struct {
	strategyList []strategy.Strategy
	queue        []strategy.PatchList
	sdc          *data.SudokuDataController
}

func (slr *Solver) preparePatchList(patchList strategy.PatchList) strategy.PatchList {
	pl := strategy.PatchList{}
	sort.Sort(patchList)
	var lastPatch *strategy.Patch
	for _, patch := range patchList {
		if lastPatch == nil {
			pl = append(pl, patch)
			lastPatch = patch
			continue
		}
		if patch.GetUUID() == lastPatch.GetUUID() {
			lastPatch.StrategyNames = append(lastPatch.StrategyNames, patch.StrategyNames...)
			//lastPatch.Efficieny += patch.Efficieny
		} else {
			pl = append(pl, patch)
			lastPatch = patch
		}
	}
	return pl
}
func (slr *Solver) getNewPatchList() strategy.PatchList {
	pl := strategy.PatchList{}
	for _, st := range slr.strategyList {
		pl = append(pl, st.GetResult()...)
	}
	pl = slr.preparePatchList(pl)
	/*if len(pl) > 3 {
		pl = pl[:3]
	}*/
	return pl
}
func (slr *Solver) AddStrategy(st strategy.Strategy) {
	slr.strategyList = append(slr.strategyList, st)
}
func (slr *Solver) Init(sdc *data.SudokuDataController) {
	slr.queue = make([]strategy.PatchList, 0)
	slr.sdc = sdc
	for _, st := range slr.strategyList {
		st.Init(sdc)
	}
}
func (slr *Solver) Step() {
	patchList := slr.getNewPatchList()
	if len(patchList) > 0 {
		slr.apply(patchList)
	} else {
		slr.rollback()
	}
}
func (slr *Solver) apply(patchList strategy.PatchList) {
	slr.queue = append(slr.queue, patchList)
	slr.sdc.Set(patchList[0])
}
func (slr *Solver) rollback() {
	var success bool = false
	for !success {
		if len(slr.queue) < 1 {
			panic("Empty queue")
		}
		n := len(slr.queue)
		slr.sdc.Unset(slr.queue[n-1][0])
		slr.queue[n-1] = slr.queue[n-1][1:]
		if len(slr.queue[n-1]) < 1 {
			slr.queue = slr.queue[:n-1]
		} else {
			slr.sdc.Set(slr.queue[n-1][0])
			success = true
			break
		}
	}
}
func (slr *Solver) Solve(sdc *data.SudokuDataController) {
	slr.Init(sdc)
	for !sdc.IsSolved() {
		slr.Step()
	}
}
