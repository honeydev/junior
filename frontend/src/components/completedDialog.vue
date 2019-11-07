<template>
    <div class="col-8 offset-2">
    <div class="card">
        <div class="card-body">
            <div class="card-title">Тест пройден</div>
            <div class="d-flex justify-content-center">
                <button v-if="unsave" button class="btn btn-warning" type="button" disabled>
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    <span>{{ waitMessage }}</span>
                </button>
                <button v-else :click="redirectOnIndex" class="btn btn-success" type="button">
                    <span>{{ successMessage }}</span>
                </button>
            </div>
        </div>
    </div>
    </div>
</template>

<script>

import { eventBus } from '../eventBus.js';
import stateStorage from '../stateSorage';

export default {
    'name': 'CompletedDialog',
    data: () => {
        return {
            ...stateStorage.state,
            unsave: true,
            waitMessage: 'Идет сохранение данных...',
            successMessage: 'Тест упешно пройден, вернутся на главную?'
        };
    },
    created() {
        eventBus.$on('test-case-saved', () => {
            this.unsave = false;
        });
    },
    methods: {
        redirectOnIndex(event) {
            window.location.href = '/';
        }
    }
};
</script>
