package data

import (
	"testing"
)

func TestHash(t *testing.T) {
	in := "000040700031500006600037090000093025000000000950680000080310009400008630003060000"
	su := new(Sudoku)
	su.LoadFromHashStr(in)
	out := su.GetHashStr()
	if in != out {
		t.Error("in != out")
	}
}
func BenchmarkLoad(b *testing.B) {
	in := "000040700031500006600037090000093025000000000950680000080310009400008630003060000"
	su := new(Sudoku)
	for i := 0; i < b.N; i++ {
		su.LoadFromHashStr(in)
	}
}
