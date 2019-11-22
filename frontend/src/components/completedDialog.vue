<template>
    <div class="col-8 offset-2">
    <div class="card">
        <div class="card-body">
            <div class="card-title">Тест пройден</div>
            <div class="d-flex justify-content-center">
                <button :click="redirectOnIndex" class="btn btn-success" type="button">
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
            waitMessage: 'Идет сохранение данных...',
            successMessage: 'Тест упешно пройден, вернуться на главную?'
        };
    },
    methods: {
        redirectOnIndex(event) {
            window.location.href = '/';
        }
    }
};
</script>
