<script lang="ts">
    import { Router, Route } from 'svelte-routing';
    import Header from './components/Header.svelte';
    import Footer from './components/Footer.svelte';
    import AdminPage from './pages/Admin page.svelte';
    import Login from './pages/Login.svelte';
</script>

<Router>
    <Route path="/" component={Login} />
    <Route path="/admin" component={AdminPage} />
</Router>