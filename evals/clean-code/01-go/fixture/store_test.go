package labelstore

import "testing"

func TestLookupLabelTrimsWhitespace(t *testing.T) {
	got, err := LookupLabel(func() (string, error) { return " north ", nil })
	if err != nil || got != "north" {
		t.Fatalf("LookupLabel() = %q, %v; want north, nil", got, err)
	}
}
