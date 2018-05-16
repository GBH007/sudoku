package data

import (
	"strings"
	"testing"
)

type testPatch struct {
	row, col, num int
}

func (t *testPatch) Row() int    { return t.row }
func (t *testPatch) Column() int { return t.col }
func (t *testPatch) Number() int { return t.num }
func BenchmarkSetUnset(b *testing.B) {
	su := new(Sudoku)
	su.LoadFromHashStr(strings.Repeat("0", 81))
	sdc := NewSudokuDataController(su)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		sdc.set(0, 0, 1)
		sdc.unset(0, 0, 1)
	}
}
func BenchmarkSetUnsetPatch(b *testing.B) {
	su := new(Sudoku)
	su.LoadFromHashStr(strings.Repeat("0", 81))
	sdc := NewSudokuDataController(su)
	patch := &testPatch{0, 0, 1}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		sdc.Set(patch)
		sdc.Unset(patch)
	}
}
