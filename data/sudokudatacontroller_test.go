package data

import (
	"strings"
	"testing"
)

func BenchmarkSetUnset(b *testing.B) {
	su := new(Sudoku)
	su.LoadFromHashStr(strings.Repeat("0", 81))
	sdc := NewCacheController(su)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		sdc.set(0, 0, 1)
		sdc.unset(0, 0, 1)
	}
}
