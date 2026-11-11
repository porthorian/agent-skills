package labelstore

import (
	"fmt"
	"strings"
)

func LookupLabel(read func() (string, error)) (string, error) {
	value, err := read()
	if err != nil {
		return "", fmt.Errorf("lookup label: %v", err)
	}
	return strings.TrimSpace(value), nil
}
