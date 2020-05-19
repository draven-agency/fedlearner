package workload

import (
	"context"
	"errors"

	"github.com/crossplane/oam-kubernetes-runtime/pkg/oam"

	"github.com/draven-agency/fedlearner/deploy/kubernetes_operator/pkg/apis/fedlearner.k8s.io/v1alpha1"
)

func Translator(ctx context.Context, w oam.Workload) ([]oam.Object, error) {
	app, ok := w.(*v1alpha1.FLApp)
	if !ok {
		return nil, errors.New("invalid type")
	}

	return []oam.Object{app}, nil
}
