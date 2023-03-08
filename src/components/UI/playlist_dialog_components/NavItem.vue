<template>
  <li class="nav-item">
    <button
      href="#"
      class="nav-link text-white py-3 border-bottom w-100"
      aria-current="page"
      title=""
    >
      <span>
        {{ name }}
      </span>
    </button>
  </li>
</template>

<script>

export default {
    data() {
        return {

        }
    },
    props: {
        id: {
          type: Number,
          required: true
        },
        name: {
            type: String,
            default: 'Country playlist'
        }
    }
}
</script>
