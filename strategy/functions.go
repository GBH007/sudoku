package strategy

func getMaxElementIndexFromStart(l []int, start int) int {
	ind := start
	element := l[ind]
	for i := start + 1; i < len(l); i++ {
		if l[i] > element {
			element = l[i]
			ind = i
		}
	}
	return ind
}
