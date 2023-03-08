<template>
    <li>
        <div class="d-flex justify-content-between font-smaller">
            <div>
                <span class="name-color">{{ name }}</span>
                <span class="ms-1 text-white text-break">{{ comment }}</span>
            </div>
            <div>
                <span class="name-color">{{ time }}</span>
            </div>
        </div>
    </li>
</template>

<script>
    export default {
        props: {
            name: {
                type: String,
                required: true
            },
            comment: {
                type: String,
                required: true
            },
            time: {
                type: String,
                required: true
            }
        }
    }
</script>

<style>
    .name-color {
        color: grey;
    }
    .time-color {
        color: #383e4c;
    }
    .font-smaller {
        font-size: 13px;
    }
</style>