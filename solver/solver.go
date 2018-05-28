package solver

import (
	"sort"
	"sudoku/data"
)

type Strategy interface {
	Init(c *data.Controller)
	GetResult() []*data.Patch
	Name() string
}

type Solver struct {
	strategyList []Strategy
	queue        []data.PatchList
	c            *data.Controller
	counter      int
}

func (slr *Solver) preparePatchList(patchList data.PatchList) data.PatchList {
	pl := data.PatchList{}
	sort.Sort(patchList)
	var lastPatch *data.Patch
	for _, patch := range patchList {
		if lastPatch == nil {
			pl = append(pl, patch)
			lastPatch = patch
			continue
		}
		if patch.GetUUID() == lastPatch.GetUUID() {
			lastPatch.StrategyNames = append(lastPatch.StrategyNames, patch.StrategyNames...)
		} else {
			pl = append(pl, patch)
			lastPatch = patch
		}
	}
	return pl
}
func (slr *Solver) getNewPatchList() data.PatchList {
	pl := data.PatchList{}
	for _, st := range slr.strategyList {
		pl = append(pl, st.GetResult()...)
	}
	pl = slr.preparePatchList(pl)
	return pl
}
func (slr *Solver) AddStrategy(st Strategy) {
	slr.strategyList = append(slr.strategyList, st)
}
func (slr *Solver) Init(c *data.Controller) {
	slr.counter = 0
	slr.queue = make([]data.PatchList, 0)
	slr.c = c
	for _, st := range slr.strategyList {
		st.Init(c)
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
func (slr *Solver) apply(patchList data.PatchList) {
	slr.queue = append(slr.queue, patchList)
	slr.c.Set(patchList[0])
}
func (slr *Solver) rollback() {
	var success bool = false
	for !success {
		if len(slr.queue) < 1 {
			panic("Empty queue")
		}
		n := len(slr.queue)
		slr.c.Unset(slr.queue[n-1][0])
		slr.queue[n-1] = slr.queue[n-1][1:]
		if len(slr.queue[n-1]) < 1 {
			slr.queue = slr.queue[:n-1]
		} else {
			slr.c.Set(slr.queue[n-1][0])
			success = true
			break
		}
	}
}
func (slr *Solver) Solve(c *data.Controller) {
	slr.Init(c)
	for !c.IsSolved() {
		slr.Step()
		slr.counter++
	}
}
func (slr *Solver) GetStepsCount() int {
	return slr.counter
}
